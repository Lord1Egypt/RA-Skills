package cmd

import (
	"fmt"
	"os"
	"strings"
)

func init() {
	loadDotEnv()
}

func loadDotEnv() {
	data, err := os.ReadFile(".env")
	if err != nil {
		return
	}
	for _, line := range strings.Split(string(data), "\n") {
		line = strings.TrimSpace(line)
		if line == "" || strings.HasPrefix(line, "#") {
			continue
		}
		parts := strings.SplitN(line, "=", 2)
		if len(parts) != 2 {
			continue
		}
		key := strings.TrimSpace(parts[0])
		val := strings.TrimSpace(parts[1])
		if os.Getenv(key) == "" {
			os.Setenv(key, val)
		}
	}
}

type Config struct {
	RemoteHost  string
	Username    string
	Password    string
	CompanyCode string
}

type Command struct {
	Name        string
	Description string
	Run         func(args []string) error
}

var commands []Command

func Register(cmd Command) {
	commands = append(commands, cmd)
}

func Run() {
	if len(os.Args) < 2 {
		printUsage()
		os.Exit(1)
	}

	commandName := os.Args[1]

	if commandName == "--help" || commandName == "-h" {
		printUsage()
		return
	}

	for _, cmd := range commands {
		if cmd.Name == commandName {
			if err := cmd.Run(os.Args[2:]); err != nil {
				fmt.Fprintf(os.Stderr, "Error: %v\n", err)
				os.Exit(1)
			}
			return
		}
	}

	fmt.Fprintf(os.Stderr, "Unknown command: %s\n", commandName)
	printUsage()
	os.Exit(1)
}

func printUsage() {
	fmt.Fprintf(os.Stderr, "Usage: lynx <command> [flags]\n\nCommands:\n")
	for _, cmd := range commands {
		fmt.Fprintf(os.Stderr, "  %-40s %s\n", cmd.Name, cmd.Description)
	}
	fmt.Fprintf(os.Stderr, "\nUse 'lynx <command> --help' for more info.\n")
}

func GetConfig() *Config {
	username := os.Getenv("LYNX_USERNAME")
	password := os.Getenv("LYNX_PASSWORD")
	companyCode := os.Getenv("LYNX_COMPANY_CODE")

	if username == "" {
		fmt.Fprintf(os.Stderr, "Error: LYNX_USERNAME is not set\n")
		os.Exit(1)
	}
	if password == "" {
		fmt.Fprintf(os.Stderr, "Error: LYNX_PASSWORD is not set\n")
		os.Exit(1)
	}
	if companyCode == "" {
		fmt.Fprintf(os.Stderr, "Error: LYNX_COMPANY_CODE is not set\n")
		os.Exit(1)
	}

	return &Config{
		RemoteHost:  "www.lynx-reservations.com",
		Username:    username,
		Password:    password,
		CompanyCode: companyCode,
	}
}
