package cli

import (
	"context"
	"errors"
	"fmt"
	"log/slog"
	"strings"
	"time"

	"github.com/hashicorp/go-retryablehttp"
	"golang.org/x/oauth2"

	"github.com/stozo04/google-health-cli/internal/api"
	"github.com/stozo04/google-health-cli/internal/auth"
	"github.com/stozo04/google-health-cli/internal/config"
)

// httpTimeout is the per-attempt request budget for API calls.
const httpTimeout = 30 * time.Second

// baseURLOverride, when non-empty, points the API client at a specific base URL
// instead of config's base_url. It exists only so in-package tests can redirect
// the client at an httptest server; production leaves it empty (config wins).
var baseURLOverride string

// notAuthenticated is the friendly, exit-2 error returned when an API command
// finds no usable cached token (GOAL.md §8, §12). Its message is the hint the
// user should act on; main prints it to stderr.
var notAuthenticated = &ExitError{
	Code: ExitAuth,
	Err:  errNotAuthenticated{},
}

type errNotAuthenticated struct{}

func (errNotAuthenticated) Error() string {
	return "Not authenticated. Run:  google-health-cli auth login"
}

// apiClient resolves config, loads the cached token, and builds an
// authenticated, auto-refreshing API client. A missing/invalid token yields
// notAuthenticated (exit 2).
//
// The returned context carries the retry-backed base transport so the OAuth2
// client layers token injection on top of it (GOAL.md §4).
func (a *App) apiClient(ctx context.Context) (*api.Client, *config.Config, error) {
	cfg, err := a.resolveConfig()
	if err != nil {
		return nil, nil, err
	}

	tok, err := auth.LoadToken(cfg.TokenCache)
	if err != nil {
		a.logger.Warn("token cache unreadable", "path", cfg.TokenCache, "err", err)
	}
	if tok == nil {
		return nil, nil, notAuthenticated
	}

	// Fail fast (issue #6): if the cached token needs a refresh but we have no
	// OAuth client credentials to perform it, the refresh would fail far
	// downstream with a cryptic oauth2 "Could not determine client ID" error.
	// Catch it here with an actionable message. A still-valid token needs no
	// client credentials, so that path is unaffected.
	if !tok.Valid() && !cfg.HasOAuthClient() {
		return nil, nil, missingCredentialsError(cfg)
	}

	client := a.buildAPIClient(ctx, cfg, tok)
	return client, cfg, nil
}

// missingCredentialsError builds the actionable, exit-64 error returned when an
// API command must refresh an expired token but no OAuth client credentials were
// loaded. It names the discovery order so the caller knows where to put a config
// or which env var to set, instead of seeing the raw oauth2 endpoint error.
func missingCredentialsError(cfg *config.Config) error {
	var cause string
	if !cfg.ConfigExists {
		cause = "no config found"
	} else {
		cause = fmt.Sprintf("config %s has no client_id/client_secret", cfg.ConfigPath)
	}
	msg := fmt.Sprintf(
		"cannot refresh expired token: %s. Looked at: %s. "+
			"Set %s or pass --config <path> to a config.json with client_id and client_secret.",
		cause, strings.Join(cfg.SearchedPaths, ", "), config.EnvConfig,
	)
	return withCode(ExitUsage, errors.New(msg))
}

// buildAuthClient wires the retry transport + OAuth2 token transport for a
// known-present token, returning the auth.Client so callers can both make
// requests (HTTP) and force a token check (doctor). GOAL.md §4, §8.
func (a *App) buildAuthClient(ctx context.Context, cfg *config.Config, tok *oauth2.Token) *auth.Client {
	retry := retryablehttp.NewClient()
	retry.RetryMax = 3
	retry.HTTPClient.Timeout = httpTimeout
	retry.Logger = leveledLogger{a.logger}
	std := retry.StandardClient()

	// Put the retry-backed client in the context so oauth2.NewClient uses it as
	// the base transport (token injection wraps retries).
	clientCtx := context.WithValue(ctx, oauth2.HTTPClient, std)
	oauthCfg := auth.OAuthConfig(cfg.ClientID, cfg.ClientSecret, cfg.Scopes)
	return auth.NewHTTPClient(clientCtx, oauthCfg, tok, cfg.TokenCache, a.logger)
}

// buildAPIClient wires the API client for a known-present token. Shared by
// apiClient and the doctor-style token check.
func (a *App) buildAPIClient(ctx context.Context, cfg *config.Config, tok *oauth2.Token) *api.Client {
	base := baseURLOverride
	if base == "" {
		base = cfg.BaseURL
	}
	authClient := a.buildAuthClient(ctx, cfg, tok)
	return api.New(authClient.HTTP, base, cfg.User, a.logger)
}

// leveledLogger adapts *slog.Logger to retryablehttp.LeveledLogger so retry
// diagnostics flow to stderr at debug/warn level instead of stdout (GOAL.md §13).
type leveledLogger struct{ l *slog.Logger }

func (a leveledLogger) Error(msg string, kv ...any) { a.l.Error(msg, kv...) }
func (a leveledLogger) Warn(msg string, kv ...any)  { a.l.Warn(msg, kv...) }
func (a leveledLogger) Info(msg string, kv ...any)  { a.l.Debug(msg, kv...) }
func (a leveledLogger) Debug(msg string, kv ...any) { a.l.Debug(msg, kv...) }
