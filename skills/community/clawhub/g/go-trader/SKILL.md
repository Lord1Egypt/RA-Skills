# go-trader Trading Bot Control

Control the go-trader cryptocurrency trading system through natural language commands.

## Available Commands

### Status & Monitoring
- "What's my trading status?" → Check all positions and P&L
- "Show my BTC position" → Get specific asset status
- "Check trading health" → Verify go-trader is running
- "View recent trades" → Display recent trading activity
- "Show trading logs" → View system logs

### Control Commands
- "Enable momentum strategy" → Activate momentum trading
- "Disable RSI strategy" → Pause RSI strategy
- "Switch to paper trading" → Change to paper trading mode
- "Switch to live trading" → Enable live trading (WARNING)

### Risk Management
- "Emergency stop all" → Immediately halt all positions
- "Show risk status" → Display current risk metrics
- "Reset trading state" → Clear and reset trading state

## System Information
- go-trader API: localhost:8099
- Status endpoint: /status
- Health endpoint: /health

## Safety
- Always confirm before enabling live trading
- Default to paper trading mode
- Emergency stop available for urgent situations
