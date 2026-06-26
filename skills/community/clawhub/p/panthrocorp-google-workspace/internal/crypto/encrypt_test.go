package crypto

import (
	"bytes"
	"testing"
)

func TestRoundTrip(t *testing.T) {
	plaintext := []byte("refresh_token=abc123&access_token=xyz789")
	passphrase := "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2" // pragma: allowlist secret

	encrypted, err := Encrypt(plaintext, passphrase)
	if err != nil {
		t.Fatalf("Encrypt: %v", err)
	}

	decrypted, err := Decrypt(encrypted, passphrase)
	if err != nil {
		t.Fatalf("Decrypt: %v", err)
	}

	if !bytes.Equal(plaintext, decrypted) {
		t.Fatalf("round-trip failed: got %q, want %q", decrypted, plaintext)
	}
}

func TestWrongKey(t *testing.T) {
	plaintext := []byte("secret data")
	passphrase := "correct-key-material-for-testing-purposes-1234"

	encrypted, err := Encrypt(plaintext, passphrase)
	if err != nil {
		t.Fatalf("Encrypt: %v", err)
	}

	_, err = Decrypt(encrypted, "wrong-key-material-for-testing-purposes-5678")
	if err == nil {
		t.Fatal("expected error decrypting with wrong key")
	}
}

func TestTamperDetection(t *testing.T) {
	plaintext := []byte("secret data")
	passphrase := "correct-key-material-for-testing-purposes-1234"

	encrypted, err := Encrypt(plaintext, passphrase)
	if err != nil {
		t.Fatalf("Encrypt: %v", err)
	}

	// flip a byte in the ciphertext
	encrypted[len(encrypted)-1] ^= 0xff

	_, err = Decrypt(encrypted, passphrase)
	if err == nil {
		t.Fatal("expected error decrypting tampered data")
	}
}

func TestEmptyKey(t *testing.T) {
	_, err := Encrypt([]byte("data"), "")
	if err == nil {
		t.Fatal("expected error with empty key")
	}

	_, err = Decrypt([]byte("data"), "")
	if err == nil {
		t.Fatal("expected error with empty key")
	}
}

func TestCiphertextTooShort(t *testing.T) {
	_, err := Decrypt([]byte("short"), "some-key")
	if err == nil {
		t.Fatal("expected error with short ciphertext")
	}
}
