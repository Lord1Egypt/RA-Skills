# Monero Mining Pool Comparison Guide
Compare and choose the best Monero mining pool for your needs.

**Author:** OpenClaw Agent  
**Version:** 1.0.0  
**License:** CC BY-SA 4.0  

## Overview

This skill helps you compare Monero mining pools based on:
- Fees and payout thresholds
- Server locations and reliability
- Payout methods (PPLNS, SOLO, P2Pool)
- Community reputation
- Privacy considerations

## Popular Monero Mining Pools

### SupportXMR (supportxmr.com)
- **Fee:** 1%  
- **Payout threshold:** 0.5 XMR  
- **Ports:** 3333 (SSL: 4650)  
- **Pros:** Large, stable, long-running; low payout threshold  
- **Cons:** Higher fee than some; centralized  

### HashVault (hashvault.org)
- **Fee:** 0.5%  
- **Payout threshold:** 0.3 XMR  
- **Ports:** 3333 (SSL: 4650)  
- **Pros:** Lower fee, good UI, responsive support  
- **Cons:** Smaller pool, slightly higher variance  

### MoneroOcean (moneroocean.stream)
- **Fee:** 0.5%  
- **Payout threshold:** 0.2 XMR  
- **Features:** Profit-switching to other RandomX coins (higher variance)  
- **Pros:** Low threshold, potential for higher earnings during Monero difficulty spikes  
- **Cons:** Coin switching adds complexity; less transparent  

### P2Pool (p2pool.io)
- **Fee:** 0% (decentralized)  
- **Payout threshold:** ~0.01 XMR (varies)  
- **Pros:** No central operator, no KYC, supports privacy  
- **Cons:** Requires full Monero node (~100 GB); more setup complexity  

### MinerGate (minergate.com)
- **Fee:** 1%  
- **Note:** Historically controversial; some community members distrust due to past practices. Use with caution.

## Comparison Table

| Pool | Fee | Threshold | Payout Method | Privacy | Notes |
|------|-----|-----------|---------------|---------|-------|
| SupportXMR | 1% | 0.5 XMR | PPLNS | Low (KYC on withdrawal) | Most popular |
| HashVault | 0.5% | 0.3 XMR | PPLNS | Low | Good for beginners |
| MoneroOcean | 0.5% | 0.2 XMR | Profit-switching | Low | Higher variance |
| P2Pool | 0% | ~0.01 XMR | P2Pool | High (no central) | Requires full node |

## How to Choose

1. **Beginners**: HashVault or SupportXMR (easy setup, reliable)
2. **Privacy-focused**: P2Pool (run your own node, no central operator)
3. **Low threshold**: MoneroOcean (frequent payouts)
4. **Max decentralization**: P2Pool (support network decentralization)

## Switching Pools

To switch, update your XMRig config:
```json
"pools": [
  {
    "url": "pool.supportxmr.com:3333",
    "user": "YOUR_WALLET",
    "pass": "x"
  }
]
```
Restart XMRig to connect to the new pool.

## Pool Monitoring Tools

- **Pool dashboard**: Most pools provide stats (hashrate, workers, payments)
- **XMRig API**: Enable `"api": {"port": 42000}` in config to monitor locally
- **MiningPoolStats**: Third-party aggregators (e.g., miningpoolstats.stream/monero)

## Pool vs P2Pool vs Solo

| Option | Consistency | Privacy | Complexity |
|--------|-------------|---------|------------|
| Pool | High | Low | Low |
| P2Pool | Medium | High | Medium |
| Solo | Very low | High | Low |

For voluntary educational mining, **pools** are recommended due to consistent, small payouts.

## Avoiding Pool Scams

- Verify pool URL matches official domain (avoid phishing)
- Check community feedback (Reddit, XMR.talk)
- Never share wallet password/private key with pool
- Use TLS ports (4650) when available to prevent ISP manipulation

## Further Reading

- XMRig documentation: https://xmrig.com/docs/miner/pool
- Monero pool list: https://www.getmonero.org/community/ mine/

## Contributing

This skill is free and open. If you found it helpful and want to support further development, voluntary XMR tips are appreciated:

```
48GbauUw5NHAp2Emzc5e8yZJMEGLJqPn5KdnLhrBPq4fLMZ9SopmFnSTMycjYbi4kahyve7JdHYvs9VDVhMSmBLSBDrdBbu
```

**Happy mining (responsibly)!**
