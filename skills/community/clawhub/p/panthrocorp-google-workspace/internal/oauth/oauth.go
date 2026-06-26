package oauth

import (
	"context"
	"fmt"

	"golang.org/x/oauth2"
	"golang.org/x/oauth2/google"
)

// NewOAuthConfig builds an OAuth2 config for Google APIs using
// the Desktop app flow (redirect to localhost).
func NewOAuthConfig(clientID, clientSecret string, scopes []string) *oauth2.Config {
	return &oauth2.Config{
		ClientID:     clientID,
		ClientSecret: clientSecret,
		Endpoint:     google.Endpoint,
		RedirectURL:  "http://localhost",
		Scopes:       scopes,
	}
}

// InteractiveLogin performs the OAuth2 authorisation code flow for a headless
// server. It prints a URL for the user to visit, then reads the auth code
// from stdin.
func InteractiveLogin(ctx context.Context, cfg *oauth2.Config) (*oauth2.Token, error) {
	url := cfg.AuthCodeURL("state", oauth2.AccessTypeOffline, oauth2.ApprovalForce)

	fmt.Println("Visit this URL in your browser to authorise access:")
	fmt.Println()
	fmt.Println("  " + url)
	fmt.Println()
	fmt.Print("Paste the authorisation code here: ")

	var code string
	if _, err := fmt.Scan(&code); err != nil {
		return nil, fmt.Errorf("reading auth code: %w", err)
	}

	token, err := cfg.Exchange(ctx, code)
	if err != nil {
		return nil, fmt.Errorf("exchanging auth code: %w", err)
	}

	return token, nil
}
