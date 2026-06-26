package crypto

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"crypto/sha256"
	"errors"
	"fmt"
	"io"

	"golang.org/x/crypto/hkdf"
)

const (
	saltSize = 16
	keySize  = 32 // AES-256
)

// Encrypt encrypts plaintext using AES-256-GCM with a key derived via HKDF-SHA256.
// The passphrase is the raw key material (e.g. from GOOGLE_WORKSPACE_TOKEN_KEY).
// Output format: salt (16 bytes) || nonce (12 bytes) || ciphertext+tag.
func Encrypt(plaintext []byte, passphrase string) ([]byte, error) {
	if passphrase == "" {
		return nil, errors.New("encryption key must not be empty")
	}

	salt := make([]byte, saltSize)
	if _, err := io.ReadFull(rand.Reader, salt); err != nil {
		return nil, fmt.Errorf("generating salt: %w", err)
	}

	key, err := deriveKey(passphrase, salt)
	if err != nil {
		return nil, err
	}

	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, fmt.Errorf("creating cipher: %w", err)
	}

	gcm, err := cipher.NewGCM(block)
	if err != nil {
		return nil, fmt.Errorf("creating GCM: %w", err)
	}

	nonce := make([]byte, gcm.NonceSize())
	if _, err := io.ReadFull(rand.Reader, nonce); err != nil {
		return nil, fmt.Errorf("generating nonce: %w", err)
	}

	ciphertext := gcm.Seal(nil, nonce, plaintext, nil)

	// salt || nonce || ciphertext
	out := make([]byte, 0, saltSize+len(nonce)+len(ciphertext))
	out = append(out, salt...)
	out = append(out, nonce...)
	out = append(out, ciphertext...)

	return out, nil
}

// Decrypt decrypts data produced by Encrypt.
func Decrypt(data []byte, passphrase string) ([]byte, error) {
	if passphrase == "" {
		return nil, errors.New("encryption key must not be empty")
	}

	if len(data) < saltSize+12 { // salt + minimum nonce size
		return nil, errors.New("ciphertext too short")
	}

	salt := data[:saltSize]
	key, err := deriveKey(passphrase, salt)
	if err != nil {
		return nil, err
	}

	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, fmt.Errorf("creating cipher: %w", err)
	}

	gcm, err := cipher.NewGCM(block)
	if err != nil {
		return nil, fmt.Errorf("creating GCM: %w", err)
	}

	nonceSize := gcm.NonceSize()
	if len(data) < saltSize+nonceSize {
		return nil, errors.New("ciphertext too short for nonce")
	}

	nonce := data[saltSize : saltSize+nonceSize]
	ciphertext := data[saltSize+nonceSize:]

	plaintext, err := gcm.Open(nil, nonce, ciphertext, nil)
	if err != nil {
		return nil, fmt.Errorf("decryption failed (wrong key or tampered data): %w", err)
	}

	return plaintext, nil
}

func deriveKey(passphrase string, salt []byte) ([]byte, error) {
	r := hkdf.New(sha256.New, []byte(passphrase), salt, []byte("google-workspace-token"))
	key := make([]byte, keySize)
	if _, err := io.ReadFull(r, key); err != nil {
		return nil, fmt.Errorf("deriving key: %w", err)
	}
	return key, nil
}
