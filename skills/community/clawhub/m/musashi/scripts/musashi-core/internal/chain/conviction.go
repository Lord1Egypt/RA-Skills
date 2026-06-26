package chain

import (
	"context"
	"crypto/ecdsa"
	"encoding/json"
	"fmt"
	"math/big"
	"os"
	"time"

	ethereum "github.com/ethereum/go-ethereum"
	"github.com/ethereum/go-ethereum/accounts/abi/bind"
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/core/types"
	"github.com/ethereum/go-ethereum/crypto"
	"github.com/ethereum/go-ethereum/ethclient"
)

// ConvictionLog ABI function selectors
var (
	// logStrike(uint256,address,uint64,uint8,bytes32) selector — agentId is first param
	logStrikeSig = crypto.Keccak256([]byte("logStrike(uint256,address,uint64,uint8,bytes32)"))[:4]
	// recordOutcome(uint256,int128) selector
	recordOutcomeSig = crypto.Keccak256([]byte("recordOutcome(uint256,int128)"))[:4]
	// strikeCount() selector
	strikeCountSig = crypto.Keccak256([]byte("strikeCount()"))[:4]
	// reputation() selector (global)
	reputationSig = crypto.Keccak256([]byte("reputation()"))[:4]
	// setINFT(address) selector — one-time link to MusashiINFT
	setINFTSig = crypto.Keccak256([]byte("setINFT(address)"))[:4]
	// agentReputation(uint256) selector — per-agent reputation
	agentReputationSig = crypto.Keccak256([]byte("agentReputation(uint256)"))[:4]
)

// StrikeResult is the output after publishing a STRIKE on-chain.
type StrikeResult struct {
	TxHash          string `json:"tx_hash"`
	BlockNumber     uint64 `json:"block_number"`
	ContractAddress string `json:"contract_address"`
	StrikeID        string `json:"strike_id,omitempty"`
	AgentID         uint64 `json:"agent_id,omitempty"`
	ExplorerURL     string `json:"explorer_url"`
	Status          string `json:"status,omitempty"`
}

// 0G Chain defaults (override via env vars for mainnet)
const (
	DefaultOGChainRPC = "https://evmrpc-testnet.0g.ai"
	OGGalileoChainID  = 16602
	defaultExplorer   = "https://chainscan-galileo.0g.ai"
)

// OGExplorerBase returns the explorer URL, configurable via OG_EXPLORER_URL env var.
func OGExplorerBase() string {
	if url := os.Getenv("OG_EXPLORER_URL"); url != "" {
		return url
	}
	return defaultExplorer
}

// stripHexPrefix removes 0x/0X prefix from hex strings.
func stripHexPrefix(s string) string {
	if len(s) >= 2 && (s[:2] == "0x" || s[:2] == "0X") {
		return s[2:]
	}
	return s
}

// PublishStrike publishes a conviction STRIKE to the ConvictionLog contract on 0G Chain.
// If OG_CHAIN_PRIVATE_KEY is not set, returns an analysis_only result instead of an error.
func PublishStrike(agentID uint64, tokenAddress string, tokenChainID int64, convergence uint8, evidenceHash string) (string, error) {
	rpcURL := os.Getenv("OG_CHAIN_RPC")
	if rpcURL == "" {
		rpcURL = DefaultOGChainRPC
	}

	privateKeyHex := os.Getenv("OG_CHAIN_PRIVATE_KEY")
	if privateKeyHex == "" {
		result := StrikeResult{
			Status:  "analysis_only",
			AgentID: agentID,
		}
		b, _ := json.MarshalIndent(result, "", "  ")
		return string(b), nil
	}

	contractAddr := os.Getenv("CONVICTION_LOG_ADDRESS")
	if contractAddr == "" {
		return "", fmt.Errorf("CONVICTION_LOG_ADDRESS not set")
	}

	client, err := ethclient.Dial(rpcURL)
	if err != nil {
		return "", fmt.Errorf("failed to connect to 0G Chain: %w", err)
	}
	defer client.Close()

	privateKey, err := crypto.HexToECDSA(stripHexPrefix(privateKeyHex))
	if err != nil {
		return "", fmt.Errorf("invalid private key: %w", err)
	}

	publicKey := privateKey.Public()
	publicKeyECDSA, ok := publicKey.(*ecdsa.PublicKey)
	if !ok {
		return "", fmt.Errorf("error casting public key")
	}

	fromAddress := crypto.PubkeyToAddress(*publicKeyECDSA)

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	nonce, err := client.PendingNonceAt(ctx, fromAddress)
	if err != nil {
		return "", fmt.Errorf("failed to get nonce: %w", err)
	}

	gasPrice, err := client.SuggestGasPrice(ctx)
	if err != nil {
		return "", fmt.Errorf("failed to get gas price: %w", err)
	}

	chainID, err := client.ChainID(ctx)
	if err != nil {
		return "", fmt.Errorf("failed to get chain ID: %w", err)
	}

	// Encode calldata: logStrike(uint256, address, uint64, uint8, bytes32)
	token := common.HexToAddress(tokenAddress)
	evHash := common.HexToHash(evidenceHash)

	// Build ABI-encoded calldata manually — agentId (uint256) is first param
	calldata := make([]byte, 0, 4+32*5)
	calldata = append(calldata, logStrikeSig...)
	calldata = append(calldata, common.LeftPadBytes(new(big.Int).SetUint64(agentID).Bytes(), 32)...)
	calldata = append(calldata, common.LeftPadBytes(token.Bytes(), 32)...)
	calldata = append(calldata, common.LeftPadBytes(big.NewInt(tokenChainID).Bytes(), 32)...)
	calldata = append(calldata, common.LeftPadBytes([]byte{convergence}, 32)...)
	calldata = append(calldata, evHash.Bytes()...)

	contract := common.HexToAddress(contractAddr)
	tx := types.NewTransaction(nonce, contract, big.NewInt(0), 200000, gasPrice, calldata)

	signer := types.NewEIP155Signer(chainID)
	signedTx, err := types.SignTx(tx, signer, privateKey)
	if err != nil {
		return "", fmt.Errorf("failed to sign transaction: %w", err)
	}

	err = client.SendTransaction(ctx, signedTx)
	if err != nil {
		return "", fmt.Errorf("failed to send transaction: %w", err)
	}

	// Wait for receipt
	receipt, err := bind.WaitMined(ctx, client, signedTx)
	if err != nil {
		return "", fmt.Errorf("transaction not mined: %w", err)
	}
	if receipt.Status == 0 {
		return "", fmt.Errorf("transaction reverted: %s", signedTx.Hash().Hex())
	}

	result := StrikeResult{
		TxHash:          signedTx.Hash().Hex(),
		BlockNumber:     receipt.BlockNumber.Uint64(),
		ContractAddress: contractAddr,
		AgentID:         agentID,
		ExplorerURL:     fmt.Sprintf("%s/tx/%s", OGExplorerBase(), signedTx.Hash().Hex()),
	}

	b, _ := json.MarshalIndent(result, "", "  ")
	return string(b), nil
}

// ReputationResult holds on-chain reputation data.
type ReputationResult struct {
	StrikeCount    uint64 `json:"strike_count"`
	TotalFilled    uint64 `json:"total_filled"`
	Wins           uint64 `json:"wins"`
	Losses         uint64 `json:"losses"`
	TotalReturnBps int64  `json:"total_return_bps"`
	ContractAddr   string `json:"contract_address"`
	ExplorerURL    string `json:"explorer_url"`
}

// QueryReputation reads strikeCount() and reputation() from ConvictionLog.
func QueryReputation() (string, error) {
	rpcURL := os.Getenv("OG_CHAIN_RPC")
	if rpcURL == "" {
		rpcURL = DefaultOGChainRPC
	}

	contractAddr := os.Getenv("CONVICTION_LOG_ADDRESS")
	if contractAddr == "" {
		return "", fmt.Errorf("CONVICTION_LOG_ADDRESS not set")
	}

	client, err := ethclient.Dial(rpcURL)
	if err != nil {
		return "", fmt.Errorf("failed to connect to 0G Chain: %w", err)
	}
	defer client.Close()

	ctx, cancel := context.WithTimeout(context.Background(), 15*time.Second)
	defer cancel()

	contract := common.HexToAddress(contractAddr)

	// Call strikeCount()
	scResult, err := client.CallContract(ctx, ethereum.CallMsg{
		To:   &contract,
		Data: strikeCountSig,
	}, nil)
	if err != nil {
		return "", fmt.Errorf("strikeCount() call failed: %w", err)
	}

	strikeCount := new(big.Int).SetBytes(scResult).Uint64()

	// Call reputation()
	repResult, err := client.CallContract(ctx, ethereum.CallMsg{
		To:   &contract,
		Data: reputationSig,
	}, nil)
	if err != nil {
		return "", fmt.Errorf("reputation() call failed: %w", err)
	}

	// reputation() returns (uint256 total, uint256 w, uint256 l, int256 totalReturn)
	var totalFilled, wins, losses uint64
	var totalReturnBps int64
	if len(repResult) >= 128 {
		totalFilled = new(big.Int).SetBytes(repResult[0:32]).Uint64()
		wins = new(big.Int).SetBytes(repResult[32:64]).Uint64()
		losses = new(big.Int).SetBytes(repResult[64:96]).Uint64()
		// Decode int256 with proper two's complement for negative values
		retVal := new(big.Int).SetBytes(repResult[96:128])
		if retVal.Bit(255) == 1 {
			retVal.Sub(retVal, new(big.Int).Lsh(big.NewInt(1), 256))
		}
		totalReturnBps = retVal.Int64()
	}

	result := ReputationResult{
		StrikeCount:    strikeCount,
		TotalFilled:    totalFilled,
		Wins:           wins,
		Losses:         losses,
		TotalReturnBps: totalReturnBps,
		ContractAddr:   contractAddr,
		ExplorerURL:    fmt.Sprintf("%s/address/%s", OGExplorerBase(), contractAddr),
	}

	b, _ := json.MarshalIndent(result, "", "  ")
	return string(b), nil
}

// AgentReputationResult holds per-agent on-chain reputation data.
type AgentReputationResult struct {
	AgentID        uint64 `json:"agent_id"`
	Strikes        uint64 `json:"strikes"`
	TotalFilled    uint64 `json:"total_filled"`
	Wins           uint64 `json:"wins"`
	Losses         uint64 `json:"losses"`
	TotalReturnBps int64  `json:"total_return_bps"`
	ContractAddr   string `json:"contract_address"`
	ExplorerURL    string `json:"explorer_url"`
}

// QueryAgentReputation reads per-agent reputation from ConvictionLog.
func QueryAgentReputation(agentID uint64) (string, error) {
	rpcURL := os.Getenv("OG_CHAIN_RPC")
	if rpcURL == "" {
		rpcURL = DefaultOGChainRPC
	}

	contractAddr := os.Getenv("CONVICTION_LOG_ADDRESS")
	if contractAddr == "" {
		return "", fmt.Errorf("CONVICTION_LOG_ADDRESS not set")
	}

	client, err := ethclient.Dial(rpcURL)
	if err != nil {
		return "", fmt.Errorf("failed to connect to 0G Chain: %w", err)
	}
	defer client.Close()

	ctx, cancel := context.WithTimeout(context.Background(), 15*time.Second)
	defer cancel()

	contract := common.HexToAddress(contractAddr)

	// Call agentReputation(uint256)
	calldata := make([]byte, 0, 4+32)
	calldata = append(calldata, agentReputationSig...)
	calldata = append(calldata, common.LeftPadBytes(new(big.Int).SetUint64(agentID).Bytes(), 32)...)

	repResult, err := client.CallContract(ctx, ethereum.CallMsg{
		To:   &contract,
		Data: calldata,
	}, nil)
	if err != nil {
		return "", fmt.Errorf("agentReputation() call failed: %w", err)
	}

	// agentReputation returns (uint256 strikes, uint256 filled, uint256 w, uint256 l, int256 totalReturn)
	var strikes, totalFilled, wins, losses uint64
	var totalReturnBps int64
	if len(repResult) >= 160 {
		strikes = new(big.Int).SetBytes(repResult[0:32]).Uint64()
		totalFilled = new(big.Int).SetBytes(repResult[32:64]).Uint64()
		wins = new(big.Int).SetBytes(repResult[64:96]).Uint64()
		losses = new(big.Int).SetBytes(repResult[96:128]).Uint64()
		// Decode int256 with proper two's complement for negative values
		retVal := new(big.Int).SetBytes(repResult[128:160])
		if retVal.Bit(255) == 1 {
			retVal.Sub(retVal, new(big.Int).Lsh(big.NewInt(1), 256))
		}
		totalReturnBps = retVal.Int64()
	}

	result := AgentReputationResult{
		AgentID:        agentID,
		Strikes:        strikes,
		TotalFilled:    totalFilled,
		Wins:           wins,
		Losses:         losses,
		TotalReturnBps: totalReturnBps,
		ContractAddr:   contractAddr,
		ExplorerURL:    fmt.Sprintf("%s/address/%s", OGExplorerBase(), contractAddr),
	}

	b, _ := json.MarshalIndent(result, "", "  ")
	return string(b), nil
}

// SetINFT links the MusashiINFT contract to ConvictionLog (one-time setup).
func SetINFT(inftAddress string) (string, error) {
	rpcURL := os.Getenv("OG_CHAIN_RPC")
	if rpcURL == "" {
		rpcURL = DefaultOGChainRPC
	}

	privateKeyHex := os.Getenv("OG_CHAIN_PRIVATE_KEY")
	if privateKeyHex == "" {
		return "", fmt.Errorf("OG_CHAIN_PRIVATE_KEY not set")
	}

	contractAddr := os.Getenv("CONVICTION_LOG_ADDRESS")
	if contractAddr == "" {
		return "", fmt.Errorf("CONVICTION_LOG_ADDRESS not set")
	}

	client, err := ethclient.Dial(rpcURL)
	if err != nil {
		return "", fmt.Errorf("failed to connect to 0G Chain: %w", err)
	}
	defer client.Close()

	privateKey, err := crypto.HexToECDSA(stripHexPrefix(privateKeyHex))
	if err != nil {
		return "", fmt.Errorf("invalid private key: %w", err)
	}

	publicKey := privateKey.Public()
	publicKeyECDSA, ok := publicKey.(*ecdsa.PublicKey)
	if !ok {
		return "", fmt.Errorf("error casting public key")
	}

	fromAddress := crypto.PubkeyToAddress(*publicKeyECDSA)

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	nonce, err := client.PendingNonceAt(ctx, fromAddress)
	if err != nil {
		return "", fmt.Errorf("failed to get nonce: %w", err)
	}

	gasPrice, err := client.SuggestGasPrice(ctx)
	if err != nil {
		return "", fmt.Errorf("failed to get gas price: %w", err)
	}

	chainID, err := client.ChainID(ctx)
	if err != nil {
		return "", fmt.Errorf("failed to get chain ID: %w", err)
	}

	// Encode calldata: setINFT(address)
	inft := common.HexToAddress(inftAddress)
	calldata := make([]byte, 0, 4+32)
	calldata = append(calldata, setINFTSig...)
	calldata = append(calldata, common.LeftPadBytes(inft.Bytes(), 32)...)

	contract := common.HexToAddress(contractAddr)
	tx := types.NewTransaction(nonce, contract, big.NewInt(0), 200000, gasPrice, calldata)

	signer := types.NewEIP155Signer(chainID)
	signedTx, err := types.SignTx(tx, signer, privateKey)
	if err != nil {
		return "", fmt.Errorf("failed to sign transaction: %w", err)
	}

	err = client.SendTransaction(ctx, signedTx)
	if err != nil {
		return "", fmt.Errorf("failed to send transaction: %w", err)
	}

	receipt, err := bind.WaitMined(ctx, client, signedTx)
	if err != nil {
		return "", fmt.Errorf("transaction not mined: %w", err)
	}
	if receipt.Status == 0 {
		return "", fmt.Errorf("transaction reverted: %s", signedTx.Hash().Hex())
	}

	result := StrikeResult{
		TxHash:          signedTx.Hash().Hex(),
		BlockNumber:     receipt.BlockNumber.Uint64(),
		ContractAddress: contractAddr,
		ExplorerURL:     fmt.Sprintf("%s/tx/%s", OGExplorerBase(), signedTx.Hash().Hex()),
	}

	b, _ := json.MarshalIndent(result, "", "  ")
	return string(b), nil
}

// RecordOutcome records the outcome of a STRIKE on-chain.
func RecordOutcome(strikeID uint64, returnBps int64) (string, error) {
	rpcURL := os.Getenv("OG_CHAIN_RPC")
	if rpcURL == "" {
		rpcURL = DefaultOGChainRPC
	}

	privateKeyHex := os.Getenv("OG_CHAIN_PRIVATE_KEY")
	if privateKeyHex == "" {
		return "", fmt.Errorf("OG_CHAIN_PRIVATE_KEY not set")
	}

	contractAddr := os.Getenv("CONVICTION_LOG_ADDRESS")
	if contractAddr == "" {
		return "", fmt.Errorf("CONVICTION_LOG_ADDRESS not set")
	}

	client, err := ethclient.Dial(rpcURL)
	if err != nil {
		return "", fmt.Errorf("failed to connect to 0G Chain: %w", err)
	}
	defer client.Close()

	privateKey, err := crypto.HexToECDSA(stripHexPrefix(privateKeyHex))
	if err != nil {
		return "", fmt.Errorf("invalid private key: %w", err)
	}

	publicKey := privateKey.Public()
	publicKeyECDSA, ok := publicKey.(*ecdsa.PublicKey)
	if !ok {
		return "", fmt.Errorf("error casting public key")
	}
	fromAddress := crypto.PubkeyToAddress(*publicKeyECDSA)

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	nonce, err := client.PendingNonceAt(ctx, fromAddress)
	if err != nil {
		return "", fmt.Errorf("failed to get nonce: %w", err)
	}

	gasPrice, err := client.SuggestGasPrice(ctx)
	if err != nil {
		return "", fmt.Errorf("failed to get gas price: %w", err)
	}

	chainID, err := client.ChainID(ctx)
	if err != nil {
		return "", fmt.Errorf("failed to get chain ID: %w", err)
	}

	// Encode: recordOutcome(uint256, int128)
	calldata := make([]byte, 0, 4+32*2)
	calldata = append(calldata, recordOutcomeSig...)
	calldata = append(calldata, common.LeftPadBytes(new(big.Int).SetUint64(strikeID).Bytes(), 32)...)

	// int128 encoding: sign-extend for negative values
	bpsBig := big.NewInt(returnBps)
	bpsBytes := bpsBig.Bytes()
	padded := make([]byte, 32)
	if returnBps < 0 {
		for i := range padded {
			padded[i] = 0xff
		}
		// Two's complement: stored in Bytes() as absolute value for negative
		abs := new(big.Int).Abs(bpsBig)
		twos := new(big.Int).Sub(new(big.Int).Lsh(big.NewInt(1), 256), abs)
		copy(padded, common.LeftPadBytes(twos.Bytes(), 32))
	} else {
		copy(padded[32-len(bpsBytes):], bpsBytes)
	}
	calldata = append(calldata, padded...)

	contract := common.HexToAddress(contractAddr)
	tx := types.NewTransaction(nonce, contract, big.NewInt(0), 200000, gasPrice, calldata)

	signer := types.NewEIP155Signer(chainID)
	signedTx, err := types.SignTx(tx, signer, privateKey)
	if err != nil {
		return "", fmt.Errorf("failed to sign transaction: %w", err)
	}

	err = client.SendTransaction(ctx, signedTx)
	if err != nil {
		return "", fmt.Errorf("failed to send transaction: %w", err)
	}

	receipt, err := bind.WaitMined(ctx, client, signedTx)
	if err != nil {
		return "", fmt.Errorf("transaction not mined: %w", err)
	}
	if receipt.Status == 0 {
		return "", fmt.Errorf("transaction reverted: %s", signedTx.Hash().Hex())
	}

	result := StrikeResult{
		TxHash:          signedTx.Hash().Hex(),
		BlockNumber:     receipt.BlockNumber.Uint64(),
		ContractAddress: contractAddr,
		ExplorerURL:     fmt.Sprintf("%s/tx/%s", OGExplorerBase(), signedTx.Hash().Hex()),
	}

	b, _ := json.MarshalIndent(result, "", "  ")
	return string(b), nil
}
