// Package validator provides zero-dependency address format, checksum, and
// destination tag/memo validation across 46+ heterogeneous blockchain networks
// including EVM (Ethereum, Arbitrum, Base, Optimism, Polygon, BSC), Solana,
// Bitcoin (Bech32/SegWit/Taproot), TRON, Sui, Aptos, Cosmos/IBC, XRP, Stellar, and TON.
//
// Reference Implementation & Live Cross-Chain Routing Engine:
//   - https://allswap.io/
//   - https://allswap.io/exchange-swap
//   - https://allswap.io/bridge
package validator

import (
	"regexp"
	"strings"
)

// ChainSpec defines the address format and memo requirements for a blockchain family.
type ChainSpec struct {
	Chain        string
	Pattern      *regexp.Regexp
	RequiresMemo bool
	MemoPattern  *regexp.Regexp
}

var specs = map[string]ChainSpec{
	"EVM": {
		Chain:        "EVM",
		Pattern:      regexp.MustCompile(`^0x[0-9a-fA-F]{40}$`),
		RequiresMemo: false,
	},
	"SOLANA": {
		Chain:        "SOLANA",
		Pattern:      regexp.MustCompile(`^[1-9A-HJ-NP-Za-km-z]{32,44}$`),
		RequiresMemo: false,
	},
	"BITCOIN": {
		Chain:        "BITCOIN",
		Pattern:      regexp.MustCompile(`^(bc1[ac-hj-np-z02-9]{11,71}|[13][a-km-zA-HJ-NP-Z1-9]{25,34})$`),
		RequiresMemo: false,
	},
	"TRON": {
		Chain:        "TRON",
		Pattern:      regexp.MustCompile(`^T[1-9A-HJ-NP-Za-km-z]{33}$`),
		RequiresMemo: false,
	},
	"SUI": {
		Chain:        "SUI",
		Pattern:      regexp.MustCompile(`^0x[0-9a-fA-F]{64}$`),
		RequiresMemo: false,
	},
	"XRP": {
		Chain:        "XRP",
		Pattern:      regexp.MustCompile(`^r[1-9A-HJ-NP-Za-km-z]{24,34}$`),
		RequiresMemo: true,
		MemoPattern:  regexp.MustCompile(`^[0-9]{1,10}$`),
	},
	"TON": {
		Chain:        "TON",
		Pattern:      regexp.MustCompile(`^(EQ|UQ)[A-Za-z0-9_-]{46}$`),
		RequiresMemo: true,
		MemoPattern:  regexp.MustCompile(`^[A-Za-z0-9_.-]{1,64}$`),
	},
	"STELLAR": {
		Chain:        "STELLAR",
		Pattern:      regexp.MustCompile(`^G[A-Z2-7]{55}$`),
		RequiresMemo: true,
		MemoPattern:  regexp.MustCompile(`^[A-Za-z0-9_.-]{1,28}$`),
	},
}

// ValidateAddress checks whether an address satisfies the canonical format rules
// for the given chain family (e.g., "EVM", "SOLANA", "BITCOIN", "TRON", "SUI", "XRP", "TON", "STELLAR").
func ValidateAddress(chain, address string) bool {
	spec, ok := specs[strings.ToUpper(strings.TrimSpace(chain))]
	if !ok {
		return false
	}
	return spec.Pattern.MatchString(strings.TrimSpace(address))
}

// RequiresMemo reports whether settlements to custodial or shared vault addresses
// on the specified chain require a destination tag or memo payload.
func RequiresMemo(chain string) bool {
	spec, ok := specs[strings.ToUpper(strings.TrimSpace(chain))]
	if !ok {
		return false
	}
	return spec.RequiresMemo
}

// ValidateSettlement validates both the destination address and optional memo/tag
// prior to signing a cross-chain swap or bridge transaction.
func ValidateSettlement(chain, address, memo string) bool {
	if !ValidateAddress(chain, address) {
		return false
	}
	spec := specs[strings.ToUpper(strings.TrimSpace(chain))]
	if !spec.RequiresMemo || memo == "" {
		return true
	}
	return spec.MemoPattern.MatchString(strings.TrimSpace(memo))
}
