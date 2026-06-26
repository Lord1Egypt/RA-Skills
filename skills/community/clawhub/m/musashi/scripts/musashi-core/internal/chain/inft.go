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

// MusashiINFT ABI function selectors
var (
	// mint(string,bytes32,bytes32)
	mintSig = crypto.Keccak256([]byte("mint(string,bytes32,bytes32)"))[:4]
	// updateIntelligence(uint256,bytes32)
	updateIntelligenceSig = crypto.Keccak256([]byte("updateIntelligence(uint256,bytes32)"))[:4]
	// getAgent(uint256)
	getAgentSig = crypto.Keccak256([]byte("getAgent(uint256)"))[:4]
	// agentCount()
	agentCountSig = crypto.Keccak256([]byte("agentCount()"))[:4]
)

// INFTResult is returned after an INFT operation.
type INFTResult struct {
	TxHash      string `json:"tx_hash"`
	BlockNumber uint64 `json:"block_number"`
	Contract    string `json:"contract_address"`
	ExplorerURL string `json:"explorer_url"`
	Action      string `json:"action"`
}

// MintAgent mints a new MUSASHI agent INFT on 0G Chain.
func MintAgent(name string, configHash string, intelligenceHash string) (string, error) {
	rpcURL := os.Getenv("OG_CHAIN_RPC")
	if rpcURL == "" {
		rpcURL = DefaultOGChainRPC
	}

	privateKeyHex := os.Getenv("OG_CHAIN_PRIVATE_KEY")
	if privateKeyHex == "" {
		return "", fmt.Errorf("OG_CHAIN_PRIVATE_KEY not set")
	}

	contractAddr := os.Getenv("MUSASHI_INFT_ADDRESS")
	if contractAddr == "" {
		return "", fmt.Errorf("MUSASHI_INFT_ADDRESS not set")
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

	// ABI-encode mint(string, bytes32, bytes32)
	// String encoding: offset(32) + bytes32 + bytes32 + string_length(32) + string_data(padded)
	nameBytes := []byte(name)
	nameLen := len(nameBytes)
	namePadded := make([]byte, ((nameLen+31)/32)*32)
	copy(namePadded, nameBytes)

	cfgHash := common.HexToHash(configHash)
	intHash := common.HexToHash(intelligenceHash)

	calldata := make([]byte, 0)
	calldata = append(calldata, mintSig...)
	// offset for string param (3 * 32 = 96)
	calldata = append(calldata, common.LeftPadBytes(big.NewInt(96).Bytes(), 32)...)
	calldata = append(calldata, cfgHash.Bytes()...)
	calldata = append(calldata, intHash.Bytes()...)
	// string: length + padded data
	calldata = append(calldata, common.LeftPadBytes(big.NewInt(int64(nameLen)).Bytes(), 32)...)
	calldata = append(calldata, namePadded...)

	contract := common.HexToAddress(contractAddr)
	tx := types.NewTransaction(nonce, contract, big.NewInt(0), 300000, gasPrice, calldata)

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

	result := INFTResult{
		TxHash:      signedTx.Hash().Hex(),
		BlockNumber: receipt.BlockNumber.Uint64(),
		Contract:    contractAddr,
		ExplorerURL: fmt.Sprintf("%s/tx/%s", OGExplorerBase(), signedTx.Hash().Hex()),
		Action:      "mint_agent",
	}

	b, _ := json.MarshalIndent(result, "", "  ")
	return string(b), nil
}

// UpdateAgentIntelligence updates the INFT's intelligence hash after new analysis cycles.
// If OG_CHAIN_PRIVATE_KEY is not set, returns a skip message instead of an error.
func UpdateAgentIntelligence(tokenID uint64, intelligenceHash string) (string, error) {
	rpcURL := os.Getenv("OG_CHAIN_RPC")
	if rpcURL == "" {
		rpcURL = DefaultOGChainRPC
	}

	privateKeyHex := os.Getenv("OG_CHAIN_PRIVATE_KEY")
	if privateKeyHex == "" {
		return `{"status":"skipped","reason":"OG_CHAIN_PRIVATE_KEY not set — analysis-only mode"}`, nil
	}

	contractAddr := os.Getenv("MUSASHI_INFT_ADDRESS")
	if contractAddr == "" {
		return "", fmt.Errorf("MUSASHI_INFT_ADDRESS not set")
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

	ogChainID, err := client.ChainID(ctx)
	if err != nil {
		return "", fmt.Errorf("failed to get chain ID: %w", err)
	}

	intHash := common.HexToHash(intelligenceHash)

	calldata := make([]byte, 0, 4+32*2)
	calldata = append(calldata, updateIntelligenceSig...)
	calldata = append(calldata, common.LeftPadBytes(big.NewInt(int64(tokenID)).Bytes(), 32)...)
	calldata = append(calldata, intHash.Bytes()...)

	contract := common.HexToAddress(contractAddr)
	tx := types.NewTransaction(nonce, contract, big.NewInt(0), 200000, gasPrice, calldata)

	signer := types.NewEIP155Signer(ogChainID)
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

	result := INFTResult{
		TxHash:      signedTx.Hash().Hex(),
		BlockNumber: receipt.BlockNumber.Uint64(),
		Contract:    contractAddr,
		ExplorerURL: fmt.Sprintf("%s/tx/%s", OGExplorerBase(), signedTx.Hash().Hex()),
		Action:      "update_intelligence",
	}

	b, _ := json.MarshalIndent(result, "", "  ")
	return string(b), nil
}

// AgentInfo holds on-chain agent INFT data.
type AgentInfo struct {
	TokenID          uint64 `json:"token_id"`
	Owner            string `json:"owner"`
	Active           bool   `json:"active"`
	WinRate          uint16 `json:"win_rate_bps"`
	ConfigHash       string `json:"config_hash"`
	IntelligenceHash string `json:"intelligence_hash"`
	TotalStrikes     uint64 `json:"total_strikes"`
	Name             string `json:"name"`
	AgentCount       uint64 `json:"agent_count"`
	ContractAddr     string `json:"contract_address"`
	ExplorerURL      string `json:"explorer_url"`
}

// QueryAgent reads agent info from MusashiINFT contract.
func QueryAgent(tokenID uint64) (string, error) {
	rpcURL := os.Getenv("OG_CHAIN_RPC")
	if rpcURL == "" {
		rpcURL = DefaultOGChainRPC
	}

	contractAddr := os.Getenv("MUSASHI_INFT_ADDRESS")
	if contractAddr == "" {
		return "", fmt.Errorf("MUSASHI_INFT_ADDRESS not set")
	}

	client, err := ethclient.Dial(rpcURL)
	if err != nil {
		return "", fmt.Errorf("failed to connect to 0G Chain: %w", err)
	}
	defer client.Close()

	ctx, cancel := context.WithTimeout(context.Background(), 15*time.Second)
	defer cancel()

	contract := common.HexToAddress(contractAddr)

	// Call agentCount()
	acResult, err := client.CallContract(ctx, ethereum.CallMsg{
		To:   &contract,
		Data: agentCountSig,
	}, nil)
	if err != nil {
		return "", fmt.Errorf("agentCount() call failed: %w", err)
	}
	agentCount := new(big.Int).SetBytes(acResult).Uint64()

	info := AgentInfo{
		TokenID:      tokenID,
		AgentCount:   agentCount,
		ContractAddr: contractAddr,
		ExplorerURL:  fmt.Sprintf("%s/address/%s", OGExplorerBase(), contractAddr),
	}

	// If agents exist, query the specific one
	if agentCount > 0 && tokenID < agentCount {
		calldata := make([]byte, 0, 4+32)
		calldata = append(calldata, getAgentSig...)
		calldata = append(calldata, common.LeftPadBytes(new(big.Int).SetUint64(tokenID).Bytes(), 32)...)

		agResult, err := client.CallContract(ctx, ethereum.CallMsg{
			To:   &contract,
			Data: calldata,
		}, nil)
		if err == nil && len(agResult) >= 352 {
			// getAgent returns a struct with dynamic string, ABI wraps in tuple:
			// word 0: offset to tuple data (0x20 = 32)
			// word 1+: struct fields (owner, active, winRate, convergenceAvg, configHash, intelligenceHash, totalStrikes, createdAt, updatedAt, name_offset)
			base := 32 // skip tuple offset word
			info.Owner = common.BytesToAddress(agResult[base : base+32]).Hex()
			info.Active = new(big.Int).SetBytes(agResult[base+32:base+64]).Uint64() != 0
			info.WinRate = uint16(new(big.Int).SetBytes(agResult[base+64 : base+96]).Uint64())
			// base+96:base+128 = convergenceAvg (skip)
			info.ConfigHash = common.BytesToHash(agResult[base+128 : base+160]).Hex()
			info.IntelligenceHash = common.BytesToHash(agResult[base+160 : base+192]).Hex()
			info.TotalStrikes = new(big.Int).SetBytes(agResult[base+192 : base+224]).Uint64()
			// base+224:base+256 = createdAt (skip)
			// base+256:base+288 = updatedAt (skip)
			// base+288:base+320 = name offset (relative to tuple start at `base`)
			nameOffsetRel := new(big.Int).SetBytes(agResult[base+288 : base+320]).Uint64()
			nameAbs := uint64(base) + nameOffsetRel
			if nameAbs+32 <= uint64(len(agResult)) {
				nameLen := new(big.Int).SetBytes(agResult[nameAbs : nameAbs+32]).Uint64()
				if nameAbs+32+nameLen <= uint64(len(agResult)) {
					info.Name = string(agResult[nameAbs+32 : nameAbs+32+nameLen])
				}
			}
		}
	}

	b, _ := json.MarshalIndent(info, "", "  ")
	return string(b), nil
}
