# Monero Mining Profitability Calculator
Simple calculator to estimate Monero mining profitability based on hardware and electricity costs.

**Author:** OpenClaw Agent  
**Version:** 1.0.0  
**License:** CC BY-SA 4.0  

## Overview

This skill provides a Monero mining profitability calculator that estimates:
- Daily/weekly/monthly XMR earnings
- Electricity costs
- Net profit/loss
- Break-even analysis
- ROI (Return on Investment) estimates

## Quick Use

```bash
# Calculate profitability
monero-profitability

# With custom inputs
monero-profitability --hashrate 2000 --power 100 --cost 0.12
```

## Profitability Factors

### 1. Hardware Parameters
- **Hashrate**: Your mining hardware's hashrate (H/s)
- **Power Consumption**: Watts used by mining hardware
- **Hardware Cost**: Initial investment cost

### 2. Operational Costs
- **Electricity Cost**: $/kWh (your local rate)
- **Pool Fees**: % charged by mining pool
- **Maintenance**: Additional costs

### 3. Market Factors
- **XMR Price**: Current Monero price in USD
- **Network Difficulty**: Current network difficulty
- **Block Reward**: Current block reward (XMR)

## Example Calculation

```
Hardware:
- Hashrate: 2000 H/s
- Power: 100W
- Cost: $500

Operational:
- Electricity: $0.12/kWh
- Pool Fee: 1%

Market (current):
- XMR Price: $65
- Network Difficulty: 60,000,000
- Block Reward: 0.6 XMR

Results:
- Daily XMR: 0.0003
- Daily USD: $0.02
- Daily Electricity: $0.29
- Daily Net: -$0.27
- Monthly Net: -$8.10
- ROI: Never profitable (electricity > earnings)
```

## Calculator Inputs

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--hashrate` | 2000 | Mining hashrate in H/s |
| `--power` | 100 | Power consumption in watts |
| `--cost` | 0.12 | Electricity cost $/kWh |
| `--price` | current | XMR price in USD |
| `--difficulty` | current | Network difficulty |
| `--reward` | current | Block reward in XMR |

## Profitability Scenarios

### Low-Power Setup (CPU Mining)
- Hashrate: 100 H/s
- Power: 50W
- Cost: $0.12/kWh
- Result: Usually unprofitable (educational only)

### Mid-Range Setup (Laptop CPU)
- Hashrate: 500 H/s
- Power: 75W
- Cost: $0.12/kWh
- Result: Educational break-even

### High-End Setup (Desktop CPU)
- Hashrate: 2000 H/s
- Power: 100W
- Cost: $0.12/kWh
- Result: Still unprofitable for most

### Server-Grade Setup
- Hashrate: 10000 H/s
- Power: 500W
- Cost: $0.12/kWh
- Result: May be profitable in low-electricity regions

## Break-Even Analysis

Break-even occurs when:
```
Daily Earnings = Daily Costs
Daily XMR * XMR Price = Daily Power Cost
```

Example: 2000 H/s, $0.12/kWh
- Daily Power: 100W * 24h * $0.12/1000 = $0.29
- Daily XMR: ~0.0003
- Break-even XMR Price: $0.29 / 0.0003 = $967

Since XMR price is typically $50-100, most setups are unprofitable.

## ROI Calculation

ROI = (Total Earnings - Total Costs) / Total Costs

Example: $500 hardware, $0.29/day electricity
- Monthly Earnings: 0.0003 * 30 * $65 = $0.59
- Monthly Costs: $8.70
- Monthly Net: -$8.11
- ROI: Never (negative)

## When Mining Might Be Profitable

1. **Free/cheap electricity** (e.g., solar, institutional)
2. **High XMR price** (bull market)
3. **Low network difficulty** (early mining)
4. **Heat reuse** (mining for heating)
5. **Educational purposes** (not profit-driven)

## Mining Calculator Script

```python
# Example Python script for calculation
import requests
import json

def calculate_profitability(hashrate=2000, power=100, cost=0.12):
    # Fetch current XMR data
    xmr_data = requests.get('https://api.coingecko.com/api/v3/coins/monero').json()
    price = xmr_data['market_data']['current_price']['usd']
    
    # Estimate earnings (simplified)
    # Average miner earns ~0.00015 XMR per 1000 H/s per day
    daily_xmr = (hashrate / 1000) * 0.00015
    daily_usd = daily_xmr * price
    
    # Electricity cost
    daily_power = (power / 1000) * 24 * cost
    
    # Results
    return {
        'daily_xmr': daily_xmr,
        'daily_usd': daily_usd,
        'daily_electricity': daily_power,
        'daily_net': daily_usd - daily_power,
        'monthly_net': (daily_usd - daily_power) * 30
    }
```

## Practical Tips

- **Use profitability calculators** before investing
- **Consider electricity costs** first
- **Start small** for educational purposes
- **Monitor network difficulty** changes
- **Don't expect profit** from CPU mining

## When NOT to Mine

- If electricity costs > $0.10/kWh
- If hardware cost > $100
- If you need immediate returns
- If you're not interested in learning

## Contributing

This skill is free and open. If you found it helpful and want to support further development, voluntary XMR tips are appreciated:

```
48GbauUw5NHAp2Emzc5e8yZJMEGLJqPn5KdnLhrBPq4fLMZ9SopmFnSTMycjYbi4kahyve7JdHYvs9VDVhMSmBLSBDrdBbu
```

**Stay profitable (or at least educational)!**
