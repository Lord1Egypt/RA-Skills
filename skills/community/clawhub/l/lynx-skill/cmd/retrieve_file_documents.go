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
		Name:        "retrieve-file-documents",
		Description: "Get documents for a transaction",
		Run:         runRetrieveFileDocuments,
	})
}

func runRetrieveFileDocuments(args []string) error {
	flags := flag.NewFlagSet("retrieve-file-documents", flag.ExitOnError)
	fileIdentifier := flags.String("file-identifier", "", "Numeric file identifier")
	transactionIdentifier := flags.String("transaction-identifier", "", "Transaction identifier")
	flags.Parse(args)

	if *fileIdentifier == "" {
		return fmt.Errorf("--file-identifier is required")
	}
	if *transactionIdentifier == "" {
		return fmt.Errorf("--transaction-identifier is required")
	}

	cfg := GetConfig()
	client, _, err := lynx.Login(cfg.RemoteHost, cfg.CompanyCode, cfg.Username, cfg.Password)
	if err != nil {
		return fmt.Errorf("authentication failed: %w", err)
	}

	body := gwt.BuildFileDocumentsByTransactionReferenceBody(cfg.RemoteHost, *fileIdentifier, *transactionIdentifier)
	respBody, err := lynx.DoGWTRequest(client, cfg.RemoteHost, "/lynx/service/file.rpc", body)
	if err != nil {
		return fmt.Errorf("retrieve file documents failed: %w", err)
	}

	result, err := gwt.ParseFileDocumentsResponse(respBody)
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
