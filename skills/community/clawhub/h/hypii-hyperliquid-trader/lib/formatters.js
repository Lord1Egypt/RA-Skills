/**
 * Output Formatters
 * Format responses for display
 */

export function formatPortfolio(state, isFree, remaining) {
  const equity = parseFloat(state.marginSummary?.accountValue || 0).toFixed(2);
  const available = parseFloat(state.withdrawable || 0).toFixed(2);
  const positions = state.assetPositions || [];
  
  let message = `📊 Hyperliquid Portfolio\n\n`;
  message += `💰 Equity: $${equity}\n`;
  message += `💵 Available: $${available}\n`;
  
  if (positions.length > 0) {
    message += `\n📈 Positions:\n`;
    positions.forEach(p => {
      const pos = p.position;
      const pnl = parseFloat(pos.unrealizedPnl || 0).toFixed(2);
      const pnlEmoji = parseFloat(pnl) >= 0 ? '🟢' : '🔴';
      message += `  ${pos.coin}: ${pos.szi} @ $${pos.entryPx} ${pnlEmoji} $${pnl}\n`;
    });
  } else {
    message += `\n📭 No open positions\n`;
  }
  
  if (isFree) {
    message += `\n🆓 Free call (${remaining} remaining today)`;
  }
  
  return message;
}

export function formatTradeResult(result, coin, side, size, orderType, charged) {
  let message = `🚀 Trade Executed\n\n`;
  message += `🪙 ${coin}\n`;
  message += `${side === 'buy' ? '🟢' : '🔴'} ${side.toUpperCase()} ${size}\n`;
  message += `📋 Type: ${orderType.toUpperCase()}\n`;
  
  if (result.status) {
    message += `✅ Status: ${result.status}\n`;
  }
  
  if (result.orderId) {
    message += `🆔 Order ID: ${result.orderId}\n`;
  }
  
  message += `\n💳 Charged: ${charged} USDT`;
  
  return message;
}

export function formatError(error) {
  if (typeof error === 'string') {
    return error;
  }
  
  if (error.message) {
    // Common error patterns
    if (error.message.includes('insufficient')) {
      return 'Insufficient balance for this operation';
    }
    if (error.message.includes('private key')) {
      return 'Private key required for trading operations';
    }
    if (error.message.includes('network')) {
      return 'Network error. Please try again later';
    }
    return error.message;
  }
  
  return 'An unknown error occurred';
}

export function formatStrategySummary(strategy) {
  let message = '';
  
  if (strategy.type === 'DCA') {
    message = `📊 DCA Strategy: ${strategy.coin}\n`;
    message += `💵 Amount: $${strategy.amount} / order\n`;
    message += `📅 Frequency: ${strategy.frequency}\n`;
    message += `🔢 Progress: ${strategy.executedOrders}/${strategy.totalOrders}\n`;
    message += `⏭️ Next: ${new Date(strategy.nextExecution).toLocaleDateString()}`;
  } else if (strategy.type === 'GRID') {
    message = `📈 Grid Strategy: ${strategy.coin}\n`;
    message += `📊 Range: $${strategy.lowerPrice} - $${strategy.upperPrice}\n`;
    message += `🔲 Grids: ${strategy.grids}\n`;
    message += `💵 Investment: $${strategy.totalInvestment}\n`;
    message += `📐 Grid Size: $${strategy.gridSize}`;
  }
  
  return message;
}
