package data

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
	"time"
)

const goPlusBaseURL = "https://api.gopluslabs.io/api/v1"

type GoPlusClient struct {
	client *http.Client
}

func NewGoPlusClient() *GoPlusClient {
	return &GoPlusClient{
		client: &http.Client{Timeout: 15 * time.Second},
	}
}

// TokenSecurityResponse represents the GoPlus token security API response.
type TokenSecurityResponse struct {
	Code    int                        `json:"code"`
	Message string                     `json:"message"`
	Result  map[string]TokenSecurityData `json:"result"`
}

type TokenSecurityData struct {
	// Contract safety
	IsHoneypot           string `json:"is_honeypot"`
	IsMintable           string `json:"is_mintable"`
	CanTakeBackOwnership string `json:"can_take_back_ownership"`
	IsProxy              string `json:"is_proxy"`
	IsOpenSource         string `json:"is_open_source"`
	IsBlacklisted        string `json:"is_blacklisted"`
	SlippageModifiable   string `json:"slippage_modifiable"`
	TransferPausable     string `json:"transfer_pausable"`

	// Tax
	BuyTax  string `json:"buy_tax"`
	SellTax string `json:"sell_tax"`

	// Holders (GoPlus returns these as strings)
	HolderCount   string `json:"holder_count"`
	LPHolderCount string `json:"lp_holder_count"`
	LPHolders     []LPHolder `json:"lp_holders"`

	// Ownership
	OwnerAddress  string `json:"owner_address"`
	CreatorAddress string `json:"creator_address"`

	// Misc
	IsAntiWhale string `json:"is_anti_whale"`
	TokenName   string `json:"token_name"`
	TokenSymbol string `json:"token_symbol"`
	TotalSupply string `json:"total_supply"`
}

type LPHolder struct {
	Address      string `json:"address"`
	Balance      string `json:"balance"`
	IsLocked     int    `json:"is_locked"`
	LockedDetail []struct {
		Amount  string `json:"amount"`
		EndTime string `json:"end_time"`
	} `json:"locked_detail"`
	Percent string `json:"percent"`
	Tag     string `json:"tag"`
}

// GetTokenSecurity fetches token security data from GoPlus.
func (c *GoPlusClient) GetTokenSecurity(chainID int64, address string) (*TokenSecurityData, error) {
	url := fmt.Sprintf("%s/token_security/%d?contract_addresses=%s",
		goPlusBaseURL, chainID, strings.ToLower(address))

	resp, err := c.client.Get(url)
	if err != nil {
		return nil, fmt.Errorf("goplus request failed: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("goplus error: status %d: %s", resp.StatusCode, body)
	}

	var result TokenSecurityResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("goplus decode failed: %w", err)
	}

	if result.Code != 1 {
		return nil, fmt.Errorf("goplus error: %s", result.Message)
	}

	data, ok := result.Result[strings.ToLower(address)]
	if !ok {
		return nil, fmt.Errorf("no data for address %s", address)
	}

	return &data, nil
}
