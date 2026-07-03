package main

import (
	"encoding/base64"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"strings"

	"github.com/urfave/cli/v2"
)

var validDocTypes = map[string]bool{
	"SUPP": true, "CLINT": true, "GEN": true, "INV": true,
	"AFTER": true, "EMAIL": true, "FLIGH": true, "BOOKI": true,
	"PHONE": true, "CLCOM": true,
}

func main() {
	app := &cli.App{
		Name:        "lynx",
		Usage:       "Stateless CLI for Lynx reservations system",
		Version:     "1.0.0",
		Description: "CLI tool to interact with lynx-reservations.com API. Authenticates via LYNX_USERNAME, LYNX_PASSWORD, LYNX_COMPANY_CODE env vars.",
		Commands: []*cli.Command{
			{
				Name:        "file-search-by-party-name",
				Aliases:     []string{"fspn"},
				Usage:       "Search files by party name",
				Description: "Retrieve files from Lynx by party name",
				Flags: []cli.Flag{
					&cli.StringFlag{Name: "party-name", Aliases: []string{"p"}, Required: true, Usage: "Party name to search for"},
				},
				Action: func(c *cli.Context) error {
					cfg, err := LoadConfig()
					if err != nil {
						return err
					}
					client := NewLynxClient(cfg)
					result, err := client.FileSearchByPartyName(c.String("party-name"))
					if err != nil {
						return err
					}
					printJSON(result)
					return nil
				},
			},
			{
				Name:        "file-search-by-file-reference",
				Aliases:     []string{"fsfr"},
				Usage:       "Search files by file reference",
				Description: "Retrieve files from Lynx by file reference",
				Flags: []cli.Flag{
					&cli.StringFlag{Name: "file-reference", Aliases: []string{"r"}, Required: true, Usage: "File reference to search for"},
				},
				Action: func(c *cli.Context) error {
					cfg, err := LoadConfig()
					if err != nil {
						return err
					}
					client := NewLynxClient(cfg)
					result, err := client.FileSearchByFileReference(c.String("file-reference"))
					if err != nil {
						return err
					}
					printJSON(result)
					return nil
				},
			},
			{
				Name:        "retrieve-itinerary",
				Aliases:     []string{"ri"},
				Usage:       "Retrieve itinerary for a file",
				Description: "Retrieve itinerary details for a given file identifier",
				Flags: []cli.Flag{
					&cli.StringFlag{Name: "file-identifier", Aliases: []string{"f"}, Required: true, Usage: "File identifier"},
					&cli.BoolFlag{Name: "show-cancelled", Aliases: []string{"c"}, Usage: "Include cancelled bookings in the results"},
				},
				Action: func(c *cli.Context) error {
					cfg, err := LoadConfig()
					if err != nil {
						return err
					}
					client := NewLynxClient(cfg)
					result, err := client.RetrieveItinerary(c.String("file-identifier"), c.Bool("show-cancelled"))
					if err != nil {
						return err
					}
					printJSON(result)
					return nil
				},
			},
			{
				Name:        "retrieve-file-documents",
				Aliases:     []string{"rfd"},
				Usage:       "Retrieve file documents",
				Description: "Retrieve documents for a given file and optional transaction. Omit --transaction-identifier to retrieve file-level documents.",
				Flags: []cli.Flag{
					&cli.StringFlag{Name: "file-identifier", Aliases: []string{"f"}, Required: true, Usage: "File identifier"},
					&cli.StringFlag{Name: "transaction-identifier", Aliases: []string{"t"}, Required: false, Usage: "Transaction identifier (omit for file-level documents)"},
				},
				Action: func(c *cli.Context) error {
					cfg, err := LoadConfig()
					if err != nil {
						return err
					}
					client := NewLynxClient(cfg)
					result, err := client.RetrieveFileDocuments(c.String("file-identifier"), c.String("transaction-identifier"))
					if err != nil {
						return err
					}
					printJSON(result)
					return nil
				},
			},
			{
				Name:        "file-document-save",
				Aliases:     []string{"fds"},
				Usage:       "Save file document details",
				Description: "Save document details for a file",
				Flags: []cli.Flag{
					&cli.StringFlag{Name: "file-identifier", Aliases: []string{"f"}, Required: true, Usage: "File identifier"},
					&cli.StringFlag{Name: "name", Aliases: []string{"n"}, Required: true, Usage: "Document name"},
					&cli.StringFlag{Name: "content", Aliases: []string{"c"}, Required: true, Usage: "Document content (plain text or HTML)"},
					&cli.StringFlag{Name: "type", Aliases: []string{"t"}, Required: true, Usage: "Document type"},
					&cli.StringFlag{Name: "attachment-url", Aliases: []string{"a"}, Usage: "Attachment URL (optional)"},
				},
				Action: func(c *cli.Context) error {
					docType := c.String("type")
					if !validDocTypes[docType] {
						return fmt.Errorf("invalid --type %q: must be one of SUPP, CLINT, GEN, INV, AFTER, EMAIL, FLIGH, BOOKI, PHONE, CLCOM", docType)
					}
					cfg, err := LoadConfig()
					if err != nil {
						return err
					}
					client := NewLynxClient(cfg)
					err = client.FileDocumentSave(
						c.String("file-identifier"),
						c.String("name"),
						c.String("content"),
						docType,
						c.String("attachment-url"),
					)
					if err != nil {
						return err
					}
					printJSON(map[string]interface{}{"status": "ok"})
					return nil
				},
			},
			{
				Name:        "transaction-document-save",
				Aliases:     []string{"tds"},
				Usage:       "Save transaction document details",
				Description: "Save document details for a transaction within a file",
				Flags: []cli.Flag{
					&cli.StringFlag{Name: "file-identifier", Aliases: []string{"f"}, Required: true, Usage: "File identifier"},
					&cli.StringFlag{Name: "transaction-identifier", Aliases: []string{"t"}, Required: true, Usage: "Transaction identifier"},
					&cli.StringFlag{Name: "name", Aliases: []string{"n"}, Required: true, Usage: "Document name"},
					&cli.StringFlag{Name: "content", Aliases: []string{"c"}, Required: true, Usage: "Document content (plain text or HTML)"},
					&cli.StringFlag{Name: "type", Aliases: []string{"d"}, Required: true, Usage: "Document type"},
					&cli.StringFlag{Name: "attachment-url", Aliases: []string{"a"}, Usage: "Attachment URL (optional)"},
				},
				Action: func(c *cli.Context) error {
					docType := c.String("type")
					if !validDocTypes[docType] {
						return fmt.Errorf("invalid --type %q: must be one of SUPP, CLINT, GEN, INV, AFTER, EMAIL, FLIGH, BOOKI, PHONE, CLCOM", docType)
					}
					cfg, err := LoadConfig()
					if err != nil {
						return err
					}
					client := NewLynxClient(cfg)
					err = client.TransactionDocumentSave(
						c.String("file-identifier"),
						c.String("transaction-identifier"),
						c.String("name"),
						c.String("content"),
						docType,
						c.String("attachment-url"),
					)
					if err != nil {
						return err
					}
					printJSON(map[string]interface{}{"status": "ok"})
					return nil
				},
			},
			{
				Name:        "attachment-upload",
				Aliases:     []string{"au"},
				Usage:       "Upload an attachment file",
				Description: "Upload a file attachment from disk",
				Flags: []cli.Flag{
					&cli.StringFlag{Name: "identifier", Aliases: []string{"i"}, Required: true, Usage: "Unique identifier for the attachment"},
					&cli.StringFlag{Name: "file", Aliases: []string{"f"}, Required: true, Usage: "Path to the file on disk"},
				},
				Action: func(c *cli.Context) error {
					cfg, err := LoadConfig()
					if err != nil {
						return err
					}
					client := NewLynxClient(cfg)
					filePath := c.String("file")
					fileData, err := os.ReadFile(filePath)
					if err != nil {
						return fmt.Errorf("failed to read file %s: %w", filePath, err)
					}
					binary := base64.StdEncoding.EncodeToString(fileData)
					fileName := filePath
					if idx := strings.LastIndex(fileName, "/"); idx >= 0 {
						fileName = fileName[idx+1:]
					}
					url, err := client.AttachmentUpload(
						binary,
						c.String("identifier"),
						fileName,
					)
					if err != nil {
						return err
					}
					result := map[string]string{"attachmentUrl": url}
					b, _ := json.MarshalIndent(result, "", "  ")
					fmt.Println(string(b))
					return nil
				},
			},
		},
	}

	if err := app.Run(os.Args); err != nil {
		log.Fatal(err)
	}
}
