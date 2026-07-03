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
		Name:        "file-search-by-file-reference",
		Description: "Search files by Lynx file reference",
		Run:         runFileSearchByFileReference,
	})
}

func runFileSearchByFileReference(args []string) error {
	flags := flag.NewFlagSet("file-search-by-file-reference", flag.ExitOnError)
	fileReference := flags.String("file-reference", "", "Lynx file reference (e.g. FTXXXXXXXXX)")
	flags.Parse(args)

	if *fileReference == "" {
		return fmt.Errorf("--file-reference is required")
	}

	cfg := GetConfig()
	client, _, err := lynx.Login(cfg.RemoteHost, cfg.CompanyCode, cfg.Username, cfg.Password)
	if err != nil {
		return fmt.Errorf("authentication failed: %w", err)
	}

	body := gwt.BuildFileSearchByFileReferenceBody(cfg.RemoteHost, *fileReference)
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
