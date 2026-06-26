package pipeline

import (
	"encoding/json"
	"fmt"
	"strings"
	"time"

	"github.com/yeheskieltame/musashi/scripts/musashi-core/internal/gates"
)

// PipelineResult holds the results of all gate evaluations.
type PipelineResult struct {
	Token     string          `json:"token"`
	ChainID   int64           `json:"chain_id"`
	Timestamp string          `json:"timestamp"`
	Status    string          `json:"status"` // PASS, FAIL, WARN
	FailedAt  int             `json:"failed_at,omitempty"`
	Gates     []*gates.Result `json:"gates"`
}

// JSON serializes the pipeline result.
func (p *PipelineResult) JSON() string {
	b, _ := json.MarshalIndent(p, "", "  ")
	return string(b)
}

// Pretty returns a human-readable summary.
func (p *PipelineResult) Pretty() string {
	var sb strings.Builder

	sb.WriteString(fmt.Sprintf("\n武蔵 MUSASHI — Gate Pipeline Results\n"))
	sb.WriteString(fmt.Sprintf("Token: %s | Chain: %d\n", p.Token, p.ChainID))
	sb.WriteString(fmt.Sprintf("Time:  %s\n", p.Timestamp))
	sb.WriteString(strings.Repeat("─", 60) + "\n")

	for _, g := range p.Gates {
		icon := "✓"
		switch g.Status {
		case gates.StatusFail:
			icon = "✗"
		case gates.StatusWarn:
			icon = "⚠"
		case gates.StatusSkip:
			icon = "○"
		}

		sb.WriteString(fmt.Sprintf("[%s] Gate %d: %s — %s\n", icon, g.GateNum, g.Gate, g.Status))
		if g.Reason != "" {
			sb.WriteString(fmt.Sprintf("    %s\n", g.Reason))
		}
	}

	sb.WriteString(strings.Repeat("─", 60) + "\n")
	sb.WriteString(fmt.Sprintf("Result: %s\n", p.Status))

	if p.Status == "FAIL" && p.FailedAt > 0 {
		sb.WriteString(fmt.Sprintf("Failed at Gate %d — pipeline stopped.\n", p.FailedAt))
	}

	return sb.String()
}

// RunGates executes the gate pipeline sequentially with fail-fast behavior.
// Gates 4 (social) and 5 (narrative) are agent-driven and skipped here.
func RunGates(token string, chainID int64) (*PipelineResult, error) {
	result := &PipelineResult{
		Token:     token,
		ChainID:   chainID,
		Timestamp: time.Now().UTC().Format(time.RFC3339),
		Status:    "PASS",
		Gates:     make([]*gates.Result, 0),
	}

	// Define gate sequence: 1, 2, 3, [4-5 agent], 6, 7
	gateList := []gates.Gate{
		gates.NewContractSafetyGate(),  // Gate 1
		gates.NewLiquidityGate(),       // Gate 2
		gates.NewWalletsGate(),         // Gate 3
		// Gate 4 (Social) — agent-driven, skip
		// Gate 5 (Narrative) — agent-driven, skip
		gates.NewTimingGate(),          // Gate 6
		gates.NewCrossValidationGate(), // Gate 7
	}

	for _, gate := range gateList {
		gateResult, err := gate.Evaluate(token, chainID)
		if err != nil {
			return nil, fmt.Errorf("gate %d (%s) error: %w", gate.Number(), gate.Name(), err)
		}

		result.Gates = append(result.Gates, gateResult)

		// Fail-fast: stop pipeline on first failure
		if gateResult.Status == gates.StatusFail {
			result.Status = "FAIL"
			result.FailedAt = gate.Number()
			return result, nil
		}

		// Track warnings
		if gateResult.Status == gates.StatusWarn && result.Status != "FAIL" {
			result.Status = "WARN"
		}
	}

	return result, nil
}
