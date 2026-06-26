package config

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
)

// ServiceMode controls the level of API access for a service.
type ServiceMode string

const (
	ModeOff       ServiceMode = "off"
	ModeReadOnly  ServiceMode = "readonly"
	ModeReadWrite ServiceMode = "readwrite"
)

// CalendarMode is an alias for ServiceMode retained for backwards compatibility.
type CalendarMode = ServiceMode

const (
	CalendarOff       = ModeOff
	CalendarReadOnly  = ModeReadOnly
	CalendarReadWrite = ModeReadWrite
)

// Config holds the scope configuration for the skill.
type Config struct {
	Gmail    bool        `json:"gmail"`
	Calendar ServiceMode `json:"calendar"`
	Contacts bool        `json:"contacts"`
	Drive    ServiceMode `json:"drive"`
	Docs     ServiceMode `json:"docs"`
	Sheets   ServiceMode `json:"sheets"`
}

// UnmarshalJSON handles backwards compatibility for the Drive field,
// which was previously a bool (true/false) and is now a ServiceMode string.
func (c *Config) UnmarshalJSON(data []byte) error {
	type raw struct {
		Gmail    bool            `json:"gmail"`
		Calendar ServiceMode     `json:"calendar"`
		Contacts bool            `json:"contacts"`
		Drive    json.RawMessage `json:"drive"`
		Docs     ServiceMode     `json:"docs"`
		Sheets   ServiceMode     `json:"sheets"`
	}
	var r raw
	if err := json.Unmarshal(data, &r); err != nil {
		return err
	}

	c.Gmail = r.Gmail
	c.Calendar = r.Calendar
	if c.Calendar == "" {
		c.Calendar = ModeOff
	}
	c.Contacts = r.Contacts

	c.Docs = r.Docs
	if c.Docs == "" {
		c.Docs = ModeOff
	}
	c.Sheets = r.Sheets
	if c.Sheets == "" {
		c.Sheets = ModeOff
	}

	if len(r.Drive) > 0 {
		if r.Drive[0] == 't' || r.Drive[0] == 'f' {
			var b bool
			if err := json.Unmarshal(r.Drive, &b); err != nil {
				return fmt.Errorf("parsing legacy drive bool: %w", err)
			}
			if b {
				c.Drive = ModeReadOnly
			} else {
				c.Drive = ModeOff
			}
		} else {
			var m ServiceMode
			if err := json.Unmarshal(r.Drive, &m); err != nil {
				return fmt.Errorf("parsing drive mode: %w", err)
			}
			c.Drive = m
		}
	}

	return nil
}

// DefaultConfig returns the default configuration.
func DefaultConfig() Config {
	return Config{
		Gmail:    true,
		Calendar: ModeReadOnly,
		Contacts: true,
		Drive:    ModeReadOnly,
		Docs:     ModeOff,
		Sheets:   ModeOff,
	}
}

func validateMode(name string, m ServiceMode) error {
	switch m {
	case ModeOff, ModeReadOnly, ModeReadWrite:
		return nil
	default:
		return fmt.Errorf("invalid %s mode %q: must be off, readonly, or readwrite", name, m)
	}
}

// Validate checks that the config values are within expected bounds.
func (c Config) Validate() error {
	if err := validateMode("calendar", c.Calendar); err != nil {
		return err
	}
	if err := validateMode("drive", c.Drive); err != nil {
		return err
	}
	if err := validateMode("docs", c.Docs); err != nil {
		return err
	}
	return validateMode("sheets", c.Sheets)
}

// Load reads config from the given directory. If the file does not exist,
// it returns the default config without error.
func Load(dir string) (Config, error) {
	path := filepath.Join(dir, "config.json")

	data, err := os.ReadFile(path)
	if err != nil {
		if errors.Is(err, os.ErrNotExist) {
			return DefaultConfig(), nil
		}
		return Config{}, fmt.Errorf("reading config: %w", err)
	}

	var cfg Config
	if err := json.Unmarshal(data, &cfg); err != nil {
		return Config{}, fmt.Errorf("parsing config: %w", err)
	}

	if err := cfg.Validate(); err != nil {
		return Config{}, err
	}

	return cfg, nil
}

// Save writes the config to the given directory, creating it if needed.
func Save(dir string, cfg Config) error {
	if err := cfg.Validate(); err != nil {
		return err
	}

	if err := os.MkdirAll(dir, 0o700); err != nil {
		return fmt.Errorf("creating config directory: %w", err)
	}

	data, err := json.MarshalIndent(cfg, "", "  ")
	if err != nil {
		return fmt.Errorf("marshalling config: %w", err)
	}

	data = append(data, '\n')
	path := filepath.Join(dir, "config.json")

	return os.WriteFile(path, data, 0o600)
}

// OAuthScopes returns the Google OAuth scopes needed for the current config.
func (c Config) OAuthScopes() []string {
	var scopes []string

	if c.Gmail {
		scopes = append(scopes, "https://www.googleapis.com/auth/gmail.readonly")
	}

	switch c.Calendar {
	case ModeReadOnly:
		scopes = append(scopes, "https://www.googleapis.com/auth/calendar.readonly")
	case ModeReadWrite:
		scopes = append(scopes, "https://www.googleapis.com/auth/calendar.events")
	}

	if c.Contacts {
		scopes = append(scopes, "https://www.googleapis.com/auth/contacts.readonly")
	}

	switch c.Drive {
	case ModeReadOnly:
		scopes = append(scopes, "https://www.googleapis.com/auth/drive.readonly")
	case ModeReadWrite:
		scopes = append(scopes, "https://www.googleapis.com/auth/drive")
	}

	switch c.Docs {
	case ModeReadOnly:
		scopes = append(scopes, "https://www.googleapis.com/auth/documents.readonly")
	case ModeReadWrite:
		scopes = append(scopes, "https://www.googleapis.com/auth/documents")
	}

	switch c.Sheets {
	case ModeReadOnly:
		scopes = append(scopes, "https://www.googleapis.com/auth/spreadsheets.readonly")
	case ModeReadWrite:
		scopes = append(scopes, "https://www.googleapis.com/auth/spreadsheets")
	}

	return scopes
}
