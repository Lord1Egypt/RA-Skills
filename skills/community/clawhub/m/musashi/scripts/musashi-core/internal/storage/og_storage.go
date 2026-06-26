package storage

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"strings"
	"time"
)

// ansiRegex strips ANSI escape codes from CLI output
var ansiRegex = regexp.MustCompile(`\x1b\[[0-9;]*m`)

const (
	DefaultStorageRPC     = "https://evmrpc-testnet.0g.ai"
	DefaultStorageIndexer = "https://indexer-storage-testnet-turbo.0g.ai"
	defaultStorageScan    = "https://storagescan-galileo.0g.ai"
	defaultChainExplorer  = "https://chainscan-galileo.0g.ai"
)

// hashPattern validates hex root hashes
var hashPattern = regexp.MustCompile(`^0x[0-9a-fA-F]{64}$`)

func storageScanBase() string {
	if url := os.Getenv("OG_STORAGE_SCAN_URL"); url != "" {
		return url
	}
	return defaultStorageScan
}

func chainExplorerBase() string {
	if url := os.Getenv("OG_EXPLORER_URL"); url != "" {
		return url
	}
	return defaultChainExplorer
}

// 0G Storage client via official 0g-storage-client CLI (file upload only)
type OGStorageClient struct {
	rpcURL     string
	indexer    string
	privateKey string
}

type StoreResult struct {
	RootHash    string `json:"root_hash,omitempty"`
	TxHash      string `json:"tx_hash,omitempty"`
	Status      string `json:"status"`
	ExplorerURL string `json:"explorer_url,omitempty"`
	StorageScan string `json:"storage_scan,omitempty"`
	DownloadCmd string `json:"download_cmd,omitempty"`
}

func NewOGStorageClient() *OGStorageClient {
	rpc := os.Getenv("OG_STORAGE_RPC")
	if rpc == "" {
		rpc = DefaultStorageRPC
	}
	indexer := os.Getenv("OG_STORAGE_INDEXER")
	if indexer == "" {
		indexer = DefaultStorageIndexer
	}
	return &OGStorageClient{
		rpcURL:     rpc,
		indexer:    indexer,
		privateKey: os.Getenv("OG_CHAIN_PRIVATE_KEY"),
	}
}

func HashEvidence(evidence interface{}) (string, error) {
	b, err := json.Marshal(evidence)
	if err != nil {
		return "", fmt.Errorf("failed to marshal evidence: %w", err)
	}
	hash := sha256.Sum256(b)
	return hex.EncodeToString(hash[:]), nil
}

// upload file to 0G Storage, returns merkle root hash
func (c *OGStorageClient) UploadFile(filePath string) (*StoreResult, error) {
	if c.privateKey == "" {
		hash, err := hashFile(filePath)
		if err != nil {
			return nil, err
		}
		return &StoreResult{
			RootHash: hash,
			Status:   "local_only (OG_CHAIN_PRIVATE_KEY not set)",
		}, nil
	}

	out, err := runCLI("upload",
		"--url", c.rpcURL,
		"--key", c.privateKey,
		"--indexer", c.indexer,
		"--file", filePath,
	)
	if err != nil {
		return nil, fmt.Errorf("0g-storage-client upload failed: %w\noutput: %s", err, out)
	}

	rootHash := parseRootHash(out)
	if rootHash == "" {
		return nil, fmt.Errorf("0g-storage-client upload succeeded but no root hash found in output: %s", out)
	}
	txHash := parseTxHash(out)
	explorerURL := ""
	if txHash != "" {
		explorerURL = fmt.Sprintf("%s/tx/%s", chainExplorerBase(), txHash)
	}
	downloadRoot := rootHash
	if len(downloadRoot) > 10 {
		downloadRoot = downloadRoot[2:10]
	}
	return &StoreResult{
		RootHash:    rootHash,
		TxHash:      txHash,
		Status:      "uploaded",
		ExplorerURL: explorerURL,
		StorageScan: storageScanBase() + "/history",
		DownloadCmd: fmt.Sprintf("0g-storage-client download --indexer %s --root %s --file evidence/%s.json --proof", c.indexer, rootHash, downloadRoot),
	}, nil
}

// marshal evidence JSON to temp file and upload
func (c *OGStorageClient) StoreEvidence(evidence interface{}) (*StoreResult, error) {
	b, err := json.MarshalIndent(evidence, "", "  ")
	if err != nil {
		return nil, fmt.Errorf("failed to marshal evidence: %w", err)
	}

	tmpFile := filepath.Join(os.TempDir(), fmt.Sprintf("musashi-evidence-%d.json", time.Now().Unix()))
	if err := os.WriteFile(tmpFile, b, 0600); err != nil {
		return nil, fmt.Errorf("failed to write temp file: %w", err)
	}
	defer os.Remove(tmpFile)

	return c.UploadFile(tmpFile)
}

// download file from 0G Storage by root hash (with merkle proof verification)
func (c *OGStorageClient) DownloadFile(rootHash string, outputPath string) error {
	if !hashPattern.MatchString(rootHash) {
		return fmt.Errorf("invalid root hash format: %s", rootHash)
	}
	if strings.HasPrefix(outputPath, "--") {
		return fmt.Errorf("invalid output path: %s", outputPath)
	}
	out, err := runCLI("download",
		"--indexer", c.indexer,
		"--root", rootHash,
		"--file", outputPath,
		"--proof",
	)
	if err != nil {
		return fmt.Errorf("0g-storage-client download failed: %w\noutput: %s", err, out)
	}
	return nil
}

func runCLI(args ...string) (string, error) {
	cmd := exec.Command("0g-storage-client", args...)
	out, err := cmd.CombinedOutput()
	return string(out), err
}

func parseRootHash(output string) string {
	// Strip ANSI escape codes
	clean := ansiRegex.ReplaceAllString(output, "")

	for _, line := range strings.Split(clean, "\n") {
		line = strings.TrimSpace(line)

		// Match "file uploaded, root = 0x..." pattern from 0g-storage-client
		if idx := strings.Index(line, "root = 0x"); idx != -1 {
			hash := strings.TrimSpace(line[idx+7:]) // skip "root = "
			if len(hash) >= 66 {
				return hash[:66]
			}
			return hash
		}

		// Match "root=0x..." pattern (structured log field)
		if idx := strings.Index(line, "root=0x"); idx != -1 {
			hash := line[idx+5:] // skip "root="
			// Take just the hash (66 chars: 0x + 64 hex)
			if spaceIdx := strings.IndexAny(hash, " \t\n"); spaceIdx != -1 {
				hash = hash[:spaceIdx]
			}
			if len(hash) == 66 {
				return hash
			}
		}

		// Direct hex hash on its own line
		if strings.HasPrefix(line, "0x") && len(line) == 66 {
			return line
		}
		if len(line) == 64 && isHex(line) {
			return "0x" + line
		}
	}

	// Last resort: find any 0x + 64 hex pattern in clean output
	re := regexp.MustCompile(`0x[0-9a-fA-F]{64}`)
	if matches := re.FindAllString(clean, -1); len(matches) > 0 {
		return matches[len(matches)-1] // last match is likely the final root
	}

	return ""
}

func parseTxHash(output string) string {
	clean := ansiRegex.ReplaceAllString(output, "")
	// Match "hash=0x..." pattern from 0g-storage-client log
	re := regexp.MustCompile(`hash=0x[0-9a-fA-F]{64}`)
	if match := re.FindString(clean); match != "" {
		return match[5:] // strip "hash="
	}
	return ""
}

func isHex(s string) bool {
	for _, c := range s {
		if !((c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F')) {
			return false
		}
	}
	return true
}

func hashFile(path string) (string, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return "", err
	}
	hash := sha256.Sum256(data)
	return hex.EncodeToString(hash[:]), nil
}
