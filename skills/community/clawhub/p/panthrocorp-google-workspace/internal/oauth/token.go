package oauth

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/crypto"
	"golang.org/x/oauth2"
)

const tokenFileName = "token.enc"

// StoredToken wraps an oauth2.Token with metadata.
type StoredToken struct {
	AccessToken  string    `json:"access_token"`
	TokenType    string    `json:"token_type"`
	RefreshToken string    `json:"refresh_token"`
	Expiry       time.Time `json:"expiry"`
}

// SaveToken encrypts and writes the OAuth token to disk.
func SaveToken(dir string, token *oauth2.Token, encryptionKey string) error {
	if encryptionKey == "" {
		return errors.New("GOOGLE_WORKSPACE_TOKEN_KEY is not set; refusing to store token unencrypted")
	}

	st := StoredToken{
		AccessToken:  token.AccessToken,
		TokenType:    token.TokenType,
		RefreshToken: token.RefreshToken,
		Expiry:       token.Expiry,
	}

	data, err := json.Marshal(st)
	if err != nil {
		return fmt.Errorf("marshalling token: %w", err)
	}

	encrypted, err := crypto.Encrypt(data, encryptionKey)
	if err != nil {
		return fmt.Errorf("encrypting token: %w", err)
	}

	if err := os.MkdirAll(dir, 0o700); err != nil {
		return fmt.Errorf("creating token directory: %w", err)
	}

	path := filepath.Join(dir, tokenFileName)
	return os.WriteFile(path, encrypted, 0o600)
}

// LoadToken reads and decrypts the OAuth token from disk.
func LoadToken(dir string, encryptionKey string) (*oauth2.Token, error) {
	if encryptionKey == "" {
		return nil, errors.New("GOOGLE_WORKSPACE_TOKEN_KEY is not set; cannot decrypt token")
	}

	path := filepath.Join(dir, tokenFileName)
	data, err := os.ReadFile(path)
	if err != nil {
		if errors.Is(err, os.ErrNotExist) {
			return nil, fmt.Errorf("no token found; run 'google-workspace auth login' first")
		}
		return nil, fmt.Errorf("reading token: %w", err)
	}

	decrypted, err := crypto.Decrypt(data, encryptionKey)
	if err != nil {
		return nil, fmt.Errorf("decrypting token: %w", err)
	}

	var st StoredToken
	if err := json.Unmarshal(decrypted, &st); err != nil {
		return nil, fmt.Errorf("parsing token: %w", err)
	}

	return &oauth2.Token{
		AccessToken:  st.AccessToken,
		TokenType:    st.TokenType,
		RefreshToken: st.RefreshToken,
		Expiry:       st.Expiry,
	}, nil
}

// DeleteToken removes the stored token file.
func DeleteToken(dir string) error {
	path := filepath.Join(dir, tokenFileName)
	err := os.Remove(path)
	if err != nil && !errors.Is(err, os.ErrNotExist) {
		return fmt.Errorf("removing token: %w", err)
	}
	return nil
}

// TokenExists checks whether a token file exists.
func TokenExists(dir string) bool {
	path := filepath.Join(dir, tokenFileName)
	_, err := os.Stat(path)
	return err == nil
}
