// Package smtp provides SMTP client functionality for nmail.
package smtp

import (
	"crypto/tls"
	"fmt"
	"mime"
	"net"
	"net/smtp"
	"strconv"
	"strings"
	"time"

	"github.com/harlock/nmail/internal/config"
)

// Send sends an email via SMTP (STARTTLS).
func Send(account config.Account, to, subject, body string) error {
	addr := net.JoinHostPort(account.SMTPHost, strconv.Itoa(account.SMTPPort))

	conn, err := net.Dial("tcp", addr)
	if err != nil {
		return fmt.Errorf("connecting to %s: %w", addr, err)
	}

	c, err := smtp.NewClient(conn, account.SMTPHost)
	if err != nil {
		return fmt.Errorf("creating SMTP client: %w", err)
	}
	defer c.Close()

	// STARTTLS
	if err := c.StartTLS(&tls.Config{ServerName: account.SMTPHost}); err != nil {
		return fmt.Errorf("STARTTLS failed: %w", err)
	}

	// Auth
	auth := smtp.PlainAuth("", account.Email, account.Password, account.SMTPHost)
	if err := c.Auth(auth); err != nil {
		return fmt.Errorf("authentication failed: %w", err)
	}

	// Envelope
	if err := c.Mail(account.Email); err != nil {
		return fmt.Errorf("MAIL FROM: %w", err)
	}

	recipients := strings.Split(to, ",")
	for _, r := range recipients {
		r = strings.TrimSpace(r)
		if err := c.Rcpt(r); err != nil {
			return fmt.Errorf("RCPT TO %s: %w", r, err)
		}
	}

	// Message
	w, err := c.Data()
	if err != nil {
		return fmt.Errorf("DATA: %w", err)
	}

	encodedSubject := mime.QEncoding.Encode("UTF-8", subject)
	msg := fmt.Sprintf(
		"From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: quoted-printable\r\n\r\n%s",
		account.Email,
		to,
		encodedSubject,
		time.Now().Format("Mon, 02 Jan 2006 15:04:05 -0700"),
		body,
	)

	if _, err := w.Write([]byte(msg)); err != nil {
		return fmt.Errorf("writing message: %w", err)
	}
	if err := w.Close(); err != nil {
		return fmt.Errorf("closing DATA: %w", err)
	}

	return c.Quit()
}
