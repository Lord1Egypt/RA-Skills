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
		Name:        "file-document-save",
		Description: "Save document at the file level",
		Run:         runFileDocumentSave,
	})
}

func runFileDocumentSave(args []string) error {
	flags := flag.NewFlagSet("file-document-save", flag.ExitOnError)
	fileIdentifier := flags.String("file-identifier", "", "Numeric file identifier")
	name := flags.String("name", "", "Document name")
	content := flags.String("content", "", "Document content (plain text or HTML)")
	docType := flags.String("type", "", "Document type (e.g. SUPP, INVOICE, RECEIPT)")
	attachmentURL := flags.String("attachment-url", "", "Attachment URL from attachment-upload")
	flags.Parse(args)

	if *fileIdentifier == "" {
		return fmt.Errorf("--file-identifier is required")
	}
	if *name == "" {
		return fmt.Errorf("--name is required")
	}
	if *content == "" {
		return fmt.Errorf("--content is required")
	}
	if *docType == "" {
		return fmt.Errorf("--type is required")
	}

	cfg := GetConfig()
	client, _, err := lynx.Login(cfg.RemoteHost, cfg.CompanyCode, cfg.Username, cfg.Password)
	if err != nil {
		return fmt.Errorf("authentication failed: %w", err)
	}

	body := gwt.BuildFileDocumentSaveBody(cfg.RemoteHost, *fileIdentifier, *name, *content, *docType, *attachmentURL)
	respBody, err := lynx.DoGWTRequest(client, cfg.RemoteHost, "/lynx/service/file.rpc", body)
	if err != nil {
		return fmt.Errorf("file document save failed: %w", err)
	}

	if err := gwt.ParseSaveResponse(respBody); err != nil {
		return fmt.Errorf("file document save failed: %w", err)
	}

	output, err := json.MarshalIndent(map[string]string{"status": "ok"}, "", "  ")
	if err != nil {
		return fmt.Errorf("failed to marshal JSON: %w", err)
	}

	fmt.Println(string(output))
	return nil
}
