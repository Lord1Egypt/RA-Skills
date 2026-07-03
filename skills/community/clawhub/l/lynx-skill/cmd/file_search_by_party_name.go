package cmd

import (
	"encoding/json"
	"flag"
	"fmt"

	"dodmcdund.cc/lynx-travel-agent/lynxskill/gwt"
	"dodmcdund.cc/lynx-travel-agent/lynxskill/lynx"
)

func init() {
	Register(Command{
		Name:        "file-search-by-party-name",
		Description: "Search files by customer last name (party name)",
		Run:         runFileSearchByPartyName,
	})
}

func runFileSearchByPartyName(args []string) error {
	flags := flag.NewFlagSet("file-search-by-party-name", flag.ExitOnError)
	partyName := flags.String("party-name", "", "Customer last name to search for")
	flags.Parse(args)

	if *partyName == "" {
		return fmt.Errorf("--party-name is required")
	}

	cfg := GetConfig()
	client, _, err := lynx.Login(cfg.RemoteHost, cfg.CompanyCode, cfg.Username, cfg.Password)
	if err != nil {
		return fmt.Errorf("authentication failed: %w", err)
	}

	body := gwt.BuildFileSearchByPartyNameBody(cfg.RemoteHost, *partyName)
	respBody, err := lynx.DoGWTRequest(client, cfg.RemoteHost, "/lynx/service/file.rpc", body)
	if err != nil {
		return fmt.Errorf("file search failed: %w", err)
	}

	result, err := gwt.ParseFileSearchResponse(respBody)
	if err != nil {
		return fmt.Errorf("failed to parse response: %w", err)
	}

	output, err := json.MarshalIndent(result, "", "  ")
	if err != nil {
		return fmt.Errorf("failed to marshal JSON: %w", err)
	}

	fmt.Println(string(output))
	return nil
}
