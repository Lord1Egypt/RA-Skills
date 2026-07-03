package cmd

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"strings"

	"dodmcdund.cc/lynx-travel-agent/lynxskill/lynx"
)

func init() {
	Register(Command{
		Name:        "attachment-upload",
		Description: "Upload a file attachment from disk",
		Run:         runAttachmentUpload,
	})
}

func runAttachmentUpload(args []string) error {
	flags := flag.NewFlagSet("attachment-upload", flag.ExitOnError)
	identifier := flags.String("identifier", "", "Unique identifier for the attachment")
	filePath := flags.String("file", "", "Path to the file on disk")
	flags.Parse(args)

	if *identifier == "" {
		return fmt.Errorf("--identifier is required")
	}
	if *filePath == "" {
		return fmt.Errorf("--file is required")
	}

	fileData, err := os.ReadFile(*filePath)
	if err != nil {
		return fmt.Errorf("failed to read file %s: %w", *filePath, err)
	}

	fileName := *filePath
	if idx := strings.LastIndex(fileName, "/"); idx >= 0 {
		fileName = fileName[idx+1:]
	}

	cfg := GetConfig()
	client, _, err := lynx.Login(cfg.RemoteHost, cfg.CompanyCode, cfg.Username, cfg.Password)
	if err != nil {
		return fmt.Errorf("authentication failed: %w", err)
	}

	form := &lynx.MultipartForm{
		Fields: map[string]string{
			"fileId": *identifier,
		},
		File: struct {
			FieldName string
			FileName  string
			Data      []byte
		}{
			FieldName: "file",
			FileName:  fileName,
			Data:      fileData,
		},
	}

	respBody, err := lynx.DoMultipartRequest(client, cfg.RemoteHost, "/lynx/fileDocumentUpload", form)
	if err != nil {
		return fmt.Errorf("attachment upload failed: %w", err)
	}

	attachmentURL, err := parseAttachmentResponse(respBody)
	if err != nil {
		return fmt.Errorf("invalid attachment upload response: %w", err)
	}

	output, err := json.MarshalIndent(map[string]string{"attachmentUrl": attachmentURL}, "", "  ")
	if err != nil {
		return fmt.Errorf("failed to marshal JSON: %w", err)
	}

	fmt.Println(string(output))
	return nil
}

func parseAttachmentResponse(responseBody string) (string, error) {
	trimmed := strings.TrimSpace(responseBody)
	if !strings.HasPrefix(trimmed, "SUCCESS:") {
		return "", fmt.Errorf("unexpected response format: %s", responseBody)
	}

	urlPart := strings.TrimPrefix(trimmed, "SUCCESS:")
	urlPart = strings.TrimSpace(urlPart)

	urlPart = strings.TrimSuffix(urlPart, ":")

	if urlPart == "" || !strings.HasPrefix(urlPart, "/") {
		return "", fmt.Errorf("invalid attachment URL in response: %s", responseBody)
	}

	return urlPart, nil
}


