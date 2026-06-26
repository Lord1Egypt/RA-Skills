package wire

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"os/exec"
	"strings"
	"time"

	"github.com/maxtechera/admirarr/internal/config"
)

// CheckVPNRoute verifies qBittorrent traffic routes through Gluetun.
// Checks: 1) qBit container network_mode includes "gluetun"
//
//	2) Gluetun container is healthy
func CheckVPNRoute() WireResult {
	// Check if docker is available
	if _, err := exec.LookPath("docker"); err != nil {
		return WireResult{
			Service: "gluetun",
			Target:  "qbittorrent",
			Action:  "skipped",
			Detail:  "docker not available",
		}
	}

	qbitContainer := config.ContainerName("qbittorrent")
	gluetunContainer := config.ContainerName("gluetun")

	// Check qBit container network_mode
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	out, err := exec.CommandContext(ctx, "docker", "inspect",
		"--format", "{{.HostConfig.NetworkMode}}", qbitContainer).Output()
	if err != nil {
		return WireResult{
			Service: "gluetun",
			Target:  "qbittorrent",
			Action:  "failed",
			Detail:  fmt.Sprintf("cannot inspect qBittorrent container %q: %v", qbitContainer, err),
			Err:     err,
		}
	}

	networkMode := strings.TrimSpace(string(out))
	if !strings.Contains(networkMode, gluetunContainer) && !strings.Contains(networkMode, "gluetun") {
		return WireResult{
			Service: "gluetun",
			Target:  "qbittorrent",
			Action:  "failed",
			Detail:  fmt.Sprintf("qBittorrent network_mode=%q (expected to contain %q)", networkMode, gluetunContainer),
		}
	}

	// Check Gluetun container health
	ctx2, cancel2 := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel2()

	out2, err := exec.CommandContext(ctx2, "docker", "inspect",
		"--format", "{{.State.Health.Status}}", gluetunContainer).Output()
	if err != nil {
		return WireResult{
			Service: "gluetun",
			Target:  "qbittorrent",
			Action:  "failed",
			Detail:  fmt.Sprintf("cannot inspect Gluetun container %q: %v", gluetunContainer, err),
			Err:     err,
		}
	}

	healthStatus := strings.TrimSpace(string(out2))
	if healthStatus != "healthy" {
		return WireResult{
			Service: "gluetun",
			Target:  "qbittorrent",
			Action:  "failed",
			Detail:  fmt.Sprintf("gluetun health=%s (expected healthy)", healthStatus),
		}
	}

	return WireResult{
		Service: "gluetun",
		Target:  "qbittorrent",
		Action:  "ok",
		Detail:  fmt.Sprintf("network_mode=%s, gluetun=%s", networkMode, healthStatus),
	}
}

// VPNStatus represents Gluetun's control server status.
type VPNStatus struct {
	Connected bool
	Country   string
	IP        string
	Err       error
}

// GetVPNStatus returns Gluetun's control server status.
func GetVPNStatus() VPNStatus {
	gluetunURL := config.ServiceURL("gluetun")

	client := &http.Client{Timeout: 5 * time.Second}
	resp, err := client.Get(gluetunURL + "/v1/openvpn/status")
	if err != nil {
		return VPNStatus{Err: fmt.Errorf("cannot reach Gluetun control server: %w", err)}
	}
	defer resp.Body.Close()

	var status struct {
		Status string `json:"status"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&status); err != nil {
		return VPNStatus{Err: fmt.Errorf("cannot parse Gluetun status: %w", err)}
	}

	connected := status.Status == "running"

	// Fetch public IP info
	var ip, country string
	resp2, err := client.Get(gluetunURL + "/v1/publicip/ip")
	if err == nil {
		defer resp2.Body.Close()
		var ipResp struct {
			IP      string `json:"public_ip"`
			Country string `json:"country"`
		}
		if json.NewDecoder(resp2.Body).Decode(&ipResp) == nil {
			ip = ipResp.IP
			country = ipResp.Country
		}
	}

	return VPNStatus{
		Connected: connected,
		Country:   country,
		IP:        ip,
	}
}
