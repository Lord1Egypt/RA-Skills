package main

import (
	"fmt"
	"os"
)

type Config struct {
	RemoteHost  string
	Username    string
	Password    string
	CompanyCode string
}

func LoadConfig() (*Config, error) {
	username := os.Getenv("LYNX_USERNAME")
	if username == "" {
		return nil, fmt.Errorf("LYNX_USERNAME is not set")
	}
	password := os.Getenv("LYNX_PASSWORD")
	if password == "" {
		return nil, fmt.Errorf("LYNX_PASSWORD is not set")
	}
	companyCode := os.Getenv("LYNX_COMPANY_CODE")
	if companyCode == "" {
		return nil, fmt.Errorf("LYNX_COMPANY_CODE is not set")
	}
	return &Config{
		RemoteHost:  "www.lynx-reservations.com",
		Username:    username,
		Password:    password,
		CompanyCode: companyCode,
	}, nil
}
