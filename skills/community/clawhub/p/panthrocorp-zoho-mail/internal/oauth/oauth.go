package oauth

import (
	"context"
	"fmt"
	"net/url"

	"golang.org/x/oauth2"
)

const (
	authURL  = "https://accounts.zoho.eu/oauth/v2/auth"
	tokenURL = "https://accounts.zoho.eu/oauth/v2/token"

	// RedirectURL must be registered in the Zoho API Console.
	RedirectURL = "http://localhost:8080/callback"
)

// Scopes required for full mail access.
var Scopes = []string{
	"ZohoMail.messages.ALL",
	"ZohoMail.folders.ALL",
	"ZohoMail.accounts.READ",
}

var zohoEndpoint = oauth2.Endpoint{
	AuthURL:  authURL,
	TokenURL: tokenURL,
}

// NewOAuthConfig builds an OAuth2 config for the Zoho Mail API.
func NewOAuthConfig(clientID, clientSecret string) *oauth2.Config {
	return &oauth2.Config{
		ClientID:     clientID,
		ClientSecret: clientSecret,
		Endpoint:     zohoEndpoint,
		RedirectURL:  RedirectURL,
		Scopes:       Scopes,
	}
}

// InteractiveLogin performs the OAuth2 authorisation code flow for a headless server.
// It prints a URL for the operator to visit, then reads the full redirect URL from stdin
// and extracts the authorisation code.
func InteractiveLogin(ctx context.Context, cfg *oauth2.Config) (*oauth2.Token, error) {
	authURL := cfg.AuthCodeURL("state", oauth2.AccessTypeOffline)

	fmt.Println("Visit this URL in your browser to authorise access:")
	fmt.Println()
	fmt.Println("  " + authURL)
	fmt.Println()
	fmt.Printf("After authorising, you will be redirected to %s\n", RedirectURL)
	fmt.Println("Paste the full redirect URL here: ")

	var rawURL string
	if _, err := fmt.Scan(&rawURL); err != nil {
		return nil, fmt.Errorf("reading redirect URL: %w", err)
	}

	u, err := url.Parse(rawURL)
	if err != nil {
		return nil, fmt.Errorf("parsing redirect URL: %w", err)
	}

	code := u.Query().Get("code")
	if code == "" {
		return nil, fmt.Errorf("no 'code' parameter found in redirect URL %q", rawURL)
	}

	token, err := cfg.Exchange(ctx, code)
	if err != nil {
		return nil, fmt.Errorf("exchanging authorisation code: %w", err)
	}

	return token, nil
}
