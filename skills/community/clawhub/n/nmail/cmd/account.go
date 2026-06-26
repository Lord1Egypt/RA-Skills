package cmd

import (
	"fmt"

	"github.com/harlock/nmail/internal/config"
)

func resolveAccount(accountEmail string) (*config.Account, error) {
	cfg, err := config.Load()
	if err != nil {
		return nil, err
	}
	if accountEmail == "" {
		return cfg.Default()
	}
	for i := range cfg.Accounts {
		if cfg.Accounts[i].Email == accountEmail {
			return &cfg.Accounts[i], nil
		}
	}
	return nil, fmt.Errorf("account not found: %s", accountEmail)
}
