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
		Name:        "retrieve-itinerary",
		Description: "Get detailed itinerary for a file",
		Run:         runRetrieveItinerary,
	})
}

func runRetrieveItinerary(args []string) error {
	flags := flag.NewFlagSet("retrieve-itinerary", flag.ExitOnError)
	fileIdentifier := flags.String("file-identifier", "", "Numeric file identifier")
	showCancelled := flags.Bool("show-cancelled", false, "Include cancelled bookings in the results")
	flags.Parse(args)

	if *fileIdentifier == "" {
		return fmt.Errorf("--file-identifier is required")
	}

	cfg := GetConfig()
	client, _, err := lynx.Login(cfg.RemoteHost, cfg.CompanyCode, cfg.Username, cfg.Password)
	if err != nil {
		return fmt.Errorf("authentication failed: %w", err)
	}

	body := gwt.BuildRetrieveItineraryBody(cfg.RemoteHost, *fileIdentifier, *showCancelled)
	respBody, err := lynx.DoGWTRequest(client, cfg.RemoteHost, "/lynx/service/file.rpc", body)
	if err != nil {
		return fmt.Errorf("retrieve itinerary failed: %w", err)
	}

	result, err := gwt.ParseRetrieveItineraryResponse(respBody)
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
