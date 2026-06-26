package cmd

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/config"
	"github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/oauth"
	"github.com/spf13/cobra"
)

var authCmd = &cobra.Command{
	Use:   "auth",
	Short: "Manage Google OAuth authentication",
}

var authLoginCmd = &cobra.Command{
	Use:   "login",
	Short: "Authenticate with Google (interactive OAuth flow)",
	Run: func(cmd *cobra.Command, args []string) {
		key := encryptionKey()
		if key == "" {
			exitf("GOOGLE_WORKSPACE_TOKEN_KEY environment variable is not set")
		}

		cID := clientID()
		cSecret := clientSecret()
		if cID == "" || cSecret == "" {
			exitf("GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables must be set")
		}

		cfg, err := config.Load(configDir)
		if err != nil {
			exitf("loading config: %v", err)
		}

		scopes := cfg.OAuthScopes()
		if len(scopes) == 0 {
			exitf("no services enabled in config; run 'google-workspace config set' first")
		}

		fmt.Printf("Requesting scopes: %v\n\n", scopes)

		oauthCfg := oauth.NewOAuthConfig(cID, cSecret, scopes)
		ctx := context.Background()

		token, err := oauth.InteractiveLogin(ctx, oauthCfg)
		if err != nil {
			exitf("authentication failed: %v", err)
		}

		if err := oauth.SaveToken(configDir, token, key); err != nil {
			exitf("saving token: %v", err)
		}

		fmt.Println("\nAuthentication successful. Token encrypted and stored.")
	},
}

var authStatusCmd = &cobra.Command{
	Use:   "status",
	Short: "Show current authentication status",
	Run: func(cmd *cobra.Command, args []string) {
		key := encryptionKey()
		if key == "" {
			exitf("GOOGLE_WORKSPACE_TOKEN_KEY environment variable is not set")
		}

		if !oauth.TokenExists(configDir) {
			fmt.Println("No token found. Run 'google-workspace auth login' to authenticate.")
			return
		}

		token, err := oauth.LoadToken(configDir, key)
		if err != nil {
			exitf("loading token: %v", err)
		}

		status := map[string]any{
			"authenticated": true,
			"token_type":    token.TokenType,
			"has_refresh":   token.RefreshToken != "",
			"expiry":        token.Expiry.Format(time.RFC3339),
			"expired":       token.Expiry.Before(time.Now()),
		}

		data, _ := json.MarshalIndent(status, "", "  ")
		fmt.Println(string(data))
	},
}

var authRevokeCmd = &cobra.Command{
	Use:   "revoke",
	Short: "Delete the stored OAuth token",
	Run: func(cmd *cobra.Command, args []string) {
		if err := oauth.DeleteToken(configDir); err != nil {
			exitf("revoking token: %v", err)
		}
		fmt.Println("Local token deleted. To fully revoke access, visit https://myaccount.google.com/permissions")
	},
}

func init() {
	authCmd.AddCommand(authLoginCmd, authStatusCmd, authRevokeCmd)
	rootCmd.AddCommand(authCmd)
}
