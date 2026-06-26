package wire

import (
	"fmt"
	"strings"

	"github.com/maxtechera/admirarr/internal/arr"
)

// CheckDownloadClient checks if qBittorrent is configured in an *Arr service.
// Returns result with Action="ok" if properly configured, or details about issues.
func CheckDownloadClient(service string) WireResult {
	client := arr.New(service)

	clients, err := client.DownloadClients()
	if err != nil {
		return WireResult{
			Service: service,
			Target:  "qbittorrent",
			Action:  "failed",
			Detail:  fmt.Sprintf("cannot query download clients: %v", err),
			Err:     err,
		}
	}

	// Find qBittorrent client
	var qbitClient *arr.DownloadClient
	for i := range clients {
		if clients[i].Implementation == "QBittorrent" {
			qbitClient = &clients[i]
			break
		}
	}

	if qbitClient == nil {
		return WireResult{
			Service: service,
			Target:  "qbittorrent",
			Action:  "failed",
			Detail:  "no qBittorrent download client configured",
		}
	}

	// Validate existing client settings
	host := fmt.Sprintf("%v", qbitClient.GetField("host"))
	port := qbitClient.GetField("port")

	categoryField := "movieCategory"
	if service == "sonarr" {
		categoryField = "tvCategory"
	}
	var category string
	if v := qbitClient.GetField(categoryField); v != nil {
		category = fmt.Sprintf("%v", v)
	}

	issues := []string{}
	if host != "gluetun" && host != "localhost" && host != "127.0.0.1" && host != "qbittorrent" {
		issues = append(issues, fmt.Sprintf("host=%s", host))
	}
	if fmt.Sprintf("%v", port) != "8080" {
		issues = append(issues, fmt.Sprintf("port=%v", port))
	}
	if category == "" {
		issues = append(issues, "category not set")
	}

	if len(issues) > 0 {
		return WireResult{
			Service: service,
			Target:  "qbittorrent",
			Action:  "failed",
			Detail:  fmt.Sprintf("misconfigured: %s", strings.Join(issues, ", ")),
		}
	}

	return WireResult{
		Service: service,
		Target:  "qbittorrent",
		Action:  "ok",
		Detail:  fmt.Sprintf("host=%s, port=%v, category=%s", host, port, category),
	}
}

// EnsureDownloadClient creates or fixes the qBittorrent download client in an *Arr service.
// service: "radarr" or "sonarr"
// category: "movies" or "tv-sonarr"
// expectedHost: typically "gluetun" for VPN routing
func EnsureDownloadClient(service, category, expectedHost string) WireResult {
	client := arr.New(service)

	clients, err := client.DownloadClients()
	if err != nil {
		return WireResult{
			Service: service,
			Target:  "qbittorrent",
			Action:  "failed",
			Detail:  fmt.Sprintf("cannot query download clients: %v", err),
			Err:     err,
		}
	}

	categoryField := "movieCategory"
	if service == "sonarr" {
		categoryField = "tvCategory"
	}

	// Find existing qBittorrent client
	var qbitClient *arr.DownloadClient
	for i := range clients {
		if clients[i].Implementation == "QBittorrent" {
			qbitClient = &clients[i]
			break
		}
	}

	if qbitClient == nil {
		// Create new download client from schema
		return createDownloadClient(client, service, category, categoryField, expectedHost)
	}

	// Check if existing client needs fixing
	host := fmt.Sprintf("%v", qbitClient.GetField("host"))
	port := fmt.Sprintf("%v", qbitClient.GetField("port"))
	existingCategory := ""
	if v := qbitClient.GetField(categoryField); v != nil {
		existingCategory = fmt.Sprintf("%v", v)
	}

	needsFix := false
	if host != expectedHost {
		needsFix = true
	}
	if port != "8080" {
		needsFix = true
	}
	if existingCategory != category {
		needsFix = true
	}

	if !needsFix {
		return WireResult{
			Service: service,
			Target:  "qbittorrent",
			Action:  "ok",
			Detail:  fmt.Sprintf("already configured (host=%s, category=%s)", host, existingCategory),
		}
	}

	// Fix misconfigured client
	qbitClient.SetField("host", expectedHost)
	qbitClient.SetField("port", 8080)
	qbitClient.SetField(categoryField, category)

	if err := client.UpdateDownloadClient(qbitClient); err != nil {
		return WireResult{
			Service: service,
			Target:  "qbittorrent",
			Action:  "failed",
			Detail:  fmt.Sprintf("failed to update download client: %v", err),
			Err:     err,
		}
	}

	return WireResult{
		Service: service,
		Target:  "qbittorrent",
		Action:  "updated",
		Detail:  fmt.Sprintf("fixed host=%s, port=8080, %s=%s", expectedHost, categoryField, category),
	}
}

func createDownloadClient(client *arr.Client, service, category, categoryField, expectedHost string) WireResult {
	schemas, err := client.DownloadClientSchemas()
	if err != nil {
		return WireResult{
			Service: service,
			Target:  "qbittorrent",
			Action:  "failed",
			Detail:  fmt.Sprintf("cannot get download client schema: %v", err),
			Err:     err,
		}
	}

	var schema *arr.DownloadClient
	for i := range schemas {
		if schemas[i].Implementation == "QBittorrent" {
			schema = &schemas[i]
			break
		}
	}
	if schema == nil {
		return WireResult{
			Service: service,
			Target:  "qbittorrent",
			Action:  "failed",
			Detail:  "QBittorrent schema not found in service",
		}
	}

	schema.Name = "qBittorrent"
	schema.Enable = true
	schema.Priority = 1
	schema.RemoveCompletedDownloads = true
	schema.RemoveFailedDownloads = true
	schema.SetField("host", expectedHost)
	schema.SetField("port", 8080)
	schema.SetField("username", "admin")
	schema.SetField("password", "")
	schema.SetField(categoryField, category)

	if err := client.CreateDownloadClient(schema); err != nil {
		return WireResult{
			Service: service,
			Target:  "qbittorrent",
			Action:  "failed",
			Detail:  fmt.Sprintf("failed to create download client: %v", err),
			Err:     err,
		}
	}

	return WireResult{
		Service: service,
		Target:  "qbittorrent",
		Action:  "created",
		Detail:  fmt.Sprintf("host=%s, port=8080, %s=%s", expectedHost, categoryField, category),
	}
}
