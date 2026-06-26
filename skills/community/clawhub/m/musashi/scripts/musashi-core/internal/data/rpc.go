package data

import (
	"context"
	"fmt"
	"math/big"
	"time"

	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/ethclient"
)

// RPCClient wraps go-ethereum's ethclient for on-chain reads.
type RPCClient struct {
	client  *ethclient.Client
	chainID int64
}

// ChainIDToRPC maps chain IDs to public RPC endpoints.
func ChainIDToRPC(chainID int64) string {
	switch chainID {
	case 1:
		return "https://eth.llamarpc.com"
	case 56:
		return "https://bsc-dataseed.binance.org"
	case 137:
		return "https://polygon-rpc.com"
	case 42161:
		return "https://arb1.arbitrum.io/rpc"
	case 8453:
		return "https://mainnet.base.org"
	default:
		return "https://eth.llamarpc.com"
	}
}

// NewRPCClient creates a new RPC client for the given chain.
func NewRPCClient(chainID int64) (*RPCClient, error) {
	rpcURL := ChainIDToRPC(chainID)
	client, err := ethclient.Dial(rpcURL)
	if err != nil {
		return nil, fmt.Errorf("rpc dial failed for chain %d: %w", chainID, err)
	}
	return &RPCClient{client: client, chainID: chainID}, nil
}

// Close closes the underlying RPC connection.
func (r *RPCClient) Close() {
	r.client.Close()
}

// GetBalance returns the ETH/native token balance of an address.
func (r *RPCClient) GetBalance(address string) (*big.Int, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	addr := common.HexToAddress(address)
	balance, err := r.client.BalanceAt(ctx, addr, nil)
	if err != nil {
		return nil, fmt.Errorf("get balance failed: %w", err)
	}
	return balance, nil
}

// GetCode returns the bytecode at an address (empty = EOA, non-empty = contract).
func (r *RPCClient) GetCode(address string) ([]byte, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	addr := common.HexToAddress(address)
	code, err := r.client.CodeAt(ctx, addr, nil)
	if err != nil {
		return nil, fmt.Errorf("get code failed: %w", err)
	}
	return code, nil
}

// GetBlockNumber returns the latest block number.
func (r *RPCClient) GetBlockNumber() (uint64, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	blockNum, err := r.client.BlockNumber(ctx)
	if err != nil {
		return 0, fmt.Errorf("get block number failed: %w", err)
	}
	return blockNum, nil
}

// IsContract checks if an address is a contract (has bytecode).
func (r *RPCClient) IsContract(address string) (bool, error) {
	code, err := r.GetCode(address)
	if err != nil {
		return false, err
	}
	return len(code) > 0, nil
}

// ERC20BalanceOf reads the balanceOf for an ERC20 token.
// Uses raw eth_call with the balanceOf(address) selector.
func (r *RPCClient) ERC20BalanceOf(tokenAddress, holderAddress string) (*big.Int, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	token := common.HexToAddress(tokenAddress)
	holder := common.HexToAddress(holderAddress)

	// balanceOf(address) = 0x70a08231 + padded address
	data := append([]byte{0x70, 0xa0, 0x82, 0x31}, common.LeftPadBytes(holder.Bytes(), 32)...)

	msg := map[string]interface{}{
		"to":   token.Hex(),
		"data": fmt.Sprintf("0x%x", data),
	}

	var result string
	err := r.client.Client().CallContext(ctx, &result, "eth_call", msg, "latest")
	if err != nil {
		return nil, fmt.Errorf("erc20 balanceOf failed: %w", err)
	}

	balance := new(big.Int)
	if len(result) <= 2 {
		return big.NewInt(0), nil
	}
	balance.SetString(result[2:], 16) // strip 0x prefix
	return balance, nil
}

// ERC20TotalSupply reads the totalSupply of an ERC20 token.
func (r *RPCClient) ERC20TotalSupply(tokenAddress string) (*big.Int, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	token := common.HexToAddress(tokenAddress)

	// totalSupply() = 0x18160ddd
	data := []byte{0x18, 0x16, 0x0d, 0xdd}

	msg := map[string]interface{}{
		"to":   token.Hex(),
		"data": fmt.Sprintf("0x%x", data),
	}

	var result string
	err := r.client.Client().CallContext(ctx, &result, "eth_call", msg, "latest")
	if err != nil {
		return nil, fmt.Errorf("erc20 totalSupply failed: %w", err)
	}

	supply := new(big.Int)
	if len(result) <= 2 {
		return big.NewInt(0), nil
	}
	supply.SetString(result[2:], 16)
	return supply, nil
}

// ERC20Owner reads the owner() of a token contract (if it has one).
func (r *RPCClient) ERC20Owner(tokenAddress string) (string, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	token := common.HexToAddress(tokenAddress)

	// owner() = 0x8da5cb5b
	data := []byte{0x8d, 0xa5, 0xcb, 0x5b}

	msg := map[string]interface{}{
		"to":   token.Hex(),
		"data": fmt.Sprintf("0x%x", data),
	}

	var result string
	err := r.client.Client().CallContext(ctx, &result, "eth_call", msg, "latest")
	if err != nil {
		return "", fmt.Errorf("erc20 owner failed: %w", err)
	}

	if len(result) < 66 {
		return "0x0000000000000000000000000000000000000000", nil
	}

	return "0x" + result[26:], nil
}
