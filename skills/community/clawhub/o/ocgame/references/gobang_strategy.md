# Gobang Strategy Reference

## Game Rules

- 15x15 board
- First to connect 5 stones in a row (horizontal, vertical, or diagonal) wins
- Black plays first

## AI Strategy Parameters

### Base Weights

| Parameter | Value | Description |
|-----------|-------|-------------|
| offense | 0.55 | Attack priority weight |
| live_three | 0.45 | Open three-in-a-row weight |
| chong_four | 0.65 | Four-in-a-row with one end blocked |
| defense | 0.60 | Defense priority weight |
| block_three | 0.50 | Block opponent's three |
| block_four | 0.85 | Block opponent's four (critical) |
| center_control | 0.75 | Center position importance |
| edge_avoid | 0.40 | Avoid edge positions |
| corner_avoid | 0.60 | Avoid corner positions |

### Personality Styles

| Style | Description |
|-------|-------------|
| aggressive | High attack, low defense |
| steady | Balanced attack and defense |
| defensive | High defense, opportunistic attack |
| creative | More random, unpredictable moves |

## Pattern Recognition

### Winning Patterns
- Live Four (活四): Four in a row with both ends open - guaranteed win
- Chong Four (冲四): Four in a row with one end blocked - must block or win
- Live Three (活三): Three in a row with both ends open - threat

### Defense Patterns
- Block opponent's Live Three before it becomes Live Four
- Prioritize blocking Chong Four immediately
- Control center to limit opponent's options

## Strategy Tips

1. **Opening**: Start near center for maximum flexibility
2. **Mid-game**: Balance offense and defense based on personality
3. **End-game**: Recognize winning patterns and force wins
