package cmd

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"github.com/PanthroCorp-Limited/openclaw-skills/zoho-mail/internal/oauth"
	"github.com/spf13/cobra"
)

var authCmd = &cobra.Command{
	Use:   "auth",
	Short: "Manage Zoho OAuth authentication",
}

var authLoginCmd = &cobra.Command{
	Use:   "login",
	Short: "Authenticate with Zoho (interactive OAuth flow)",
	Run: func(cmd *cobra.Command, args []string) {
		key := encryptionKey()
		if key == "" {
			exitf("ZOHO_MAIL_TOKEN_KEY environment variable is not set")
		}

		cID := clientID()
		cSecret := clientSecret()
		if cID == "" || cSecret == "" {
			exitf("ZOHO_CLIENT_ID and ZOHO_CLIENT_SECRET environment variables must be set")
		}

		oauthCfg := oauth.NewOAuthConfig(cID, cSecret)
		ctx := context.Background()

		fmt.Printf("Requesting scopes: %v\n\n", oauth.Scopes)

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
			exitf("ZOHO_MAIL_TOKEN_KEY environment variable is not set")
		}

		if !oauth.TokenExists(configDir) {
			fmt.Println("No token found. Run 'zoho-mail auth login' to authenticate.")
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
		fmt.Println("Local token deleted. To fully revoke access, visit https://accounts.zoho.eu/home#sessions")
	},
}

func init() {
	authCmd.AddCommand(authLoginCmd, authStatusCmd, authRevokeCmd)
	rootCmd.AddCommand(authCmd)
}
