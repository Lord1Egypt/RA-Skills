package google

import (
	"context"
	"errors"
	"fmt"

	"github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/config"
	"golang.org/x/oauth2"
	"google.golang.org/api/option"
	"google.golang.org/api/sheets/v4"
)

// ErrSheetsReadOnly is returned when a write operation is attempted in readonly mode.
var ErrSheetsReadOnly = errors.New("sheets is configured as readonly; change to readwrite with 'google-workspace config set --sheets=readwrite' then re-authenticate")

// SheetsClient provides access to the Google Sheets API with configurable
// read/write mode.
type SheetsClient struct {
	svc  *sheets.Service
	mode config.ServiceMode
}

// NewSheetsClient creates a Sheets API client using the provided token source.
func NewSheetsClient(ctx context.Context, ts oauth2.TokenSource, mode config.ServiceMode) (*SheetsClient, error) {
	svc, err := sheets.NewService(ctx, option.WithTokenSource(ts))
	if err != nil {
		return nil, fmt.Errorf("creating sheets service: %w", err)
	}
	return &SheetsClient{svc: svc, mode: mode}, nil
}

// GetSpreadsheet retrieves spreadsheet metadata including sheet names.
func (c *SheetsClient) GetSpreadsheet(ctx context.Context, spreadsheetID string) (*sheets.Spreadsheet, error) {
	ss, err := c.svc.Spreadsheets.Get(spreadsheetID).
		Fields("spreadsheetId,properties(title),sheets(properties(sheetId,title,index))").
		Context(ctx).
		Do()
	if err != nil {
		return nil, fmt.Errorf("getting spreadsheet %s: %w", spreadsheetID, err)
	}
	return ss, nil
}

// ReadRange reads cell values from the specified A1-notation range.
func (c *SheetsClient) ReadRange(ctx context.Context, spreadsheetID, rangeA1 string) (*sheets.ValueRange, error) {
	resp, err := c.svc.Spreadsheets.Values.Get(spreadsheetID, rangeA1).
		Context(ctx).
		Do()
	if err != nil {
		return nil, fmt.Errorf("reading range %s from %s: %w", rangeA1, spreadsheetID, err)
	}
	return resp, nil
}

// WriteRange writes cell values to the specified A1-notation range.
// When raw is true, values are stored as-is without formula evaluation.
// When raw is false, values are interpreted as if typed by a user (formulas
// are evaluated). Requires readwrite mode.
func (c *SheetsClient) WriteRange(ctx context.Context, spreadsheetID, rangeA1 string, values [][]interface{}, raw bool) error {
	if c.mode != config.ModeReadWrite {
		return ErrSheetsReadOnly
	}

	inputOption := "USER_ENTERED"
	if raw {
		inputOption = "RAW"
	}

	vr := &sheets.ValueRange{
		Range:  rangeA1,
		Values: values,
	}

	_, err := c.svc.Spreadsheets.Values.Update(spreadsheetID, rangeA1, vr).
		ValueInputOption(inputOption).
		Context(ctx).
		Do()
	if err != nil {
		return fmt.Errorf("writing range %s in %s: %w", rangeA1, spreadsheetID, err)
	}
	return nil
}
