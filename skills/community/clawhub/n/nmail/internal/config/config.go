// Package config manages nmail account configuration (~/.nmail/config.yaml).
package config

import (
	"fmt"
	"os"
	"path/filepath"

	"gopkg.in/yaml.v3"
)

// Provider represents a supported email provider.
type Provider string

const (
	ProviderNaver  Provider = "naver"
	ProviderDaum   Provider = "daum"
	ProviderKakao  Provider = "kakao"
	ProviderCustom Provider = "custom"
)

// ProviderPresets holds default IMAP/SMTP settings per provider.
var ProviderPresets = map[Provider]Account{
	ProviderNaver: {
		IMAPHost: "imap.naver.com",
		IMAPPort: 993,
		IMAPTLS:  true,
		SMTPHost: "smtp.naver.com",
		SMTPPort: 587,
	},
	ProviderDaum: {
		IMAPHost: "imap.daum.net",
		IMAPPort: 993,
		IMAPTLS:  true,
		SMTPHost: "smtp.daum.net",
		SMTPPort: 465,
	},
}

// Account holds configuration for a single email account.
type Account struct {
	Name     string   `yaml:"name"`
	Email    string   `yaml:"email"`
	Password string   `yaml:"password"` // app password (TODO: keychain)
	Provider Provider `yaml:"provider"`
	IMAPHost string   `yaml:"imap_host"`
	IMAPPort int      `yaml:"imap_port"`
	IMAPTLS  bool     `yaml:"imap_tls"`
	SMTPHost string   `yaml:"smtp_host"`
	SMTPPort int      `yaml:"smtp_port"`
}

// Config is the top-level config structure.
type Config struct {
	DefaultAccount string    `yaml:"default_account"`
	Accounts       []Account `yaml:"accounts"`
}

// configPath returns the path to the config file.
func configPath() string {
	home, _ := os.UserHomeDir()
	return filepath.Join(home, ".nmail", "config.yaml")
}

// Load reads the config file. Returns empty config if not found.
func Load() (*Config, error) {
	path := configPath()
	data, err := os.ReadFile(path)
	if os.IsNotExist(err) {
		return &Config{}, nil
	}
	if err != nil {
		return nil, fmt.Errorf("reading config: %w", err)
	}
	var cfg Config
	if err := yaml.Unmarshal(data, &cfg); err != nil {
		return nil, fmt.Errorf("parsing config: %w", err)
	}
	return &cfg, nil
}

// Save writes the config to disk.
func Save(cfg *Config) error {
	path := configPath()
	if err := os.MkdirAll(filepath.Dir(path), 0700); err != nil {
		return fmt.Errorf("creating config dir: %w", err)
	}
	data, err := yaml.Marshal(cfg)
	if err != nil {
		return fmt.Errorf("encoding config: %w", err)
	}
	if err := os.WriteFile(path, data, 0600); err != nil {
		return fmt.Errorf("writing config: %w", err)
	}
	return nil
}

// Default returns the default account. Error if none configured.
func (c *Config) Default() (*Account, error) {
	if len(c.Accounts) == 0 {
		return nil, fmt.Errorf("no accounts configured — run: nmail config add --provider naver")
	}
	if c.DefaultAccount != "" {
		for i := range c.Accounts {
			if c.Accounts[i].Email == c.DefaultAccount {
				return &c.Accounts[i], nil
			}
		}
	}
	return &c.Accounts[0], nil
}

// Add appends an account (or updates if email already exists).
func (c *Config) Add(a Account) {
	for i := range c.Accounts {
		if c.Accounts[i].Email == a.Email {
			c.Accounts[i] = a
			return
		}
	}
	c.Accounts = append(c.Accounts, a)
	if c.DefaultAccount == "" {
		c.DefaultAccount = a.Email
	}
}

// Remove deletes an account by email.
func (c *Config) Remove(email string) bool {
	for i, a := range c.Accounts {
		if a.Email == email {
			c.Accounts = append(c.Accounts[:i], c.Accounts[i+1:]...)
			if c.DefaultAccount == email && len(c.Accounts) > 0 {
				c.DefaultAccount = c.Accounts[0].Email
			}
			return true
		}
	}
	return false
}
