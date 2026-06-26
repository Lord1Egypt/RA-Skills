# Achievements & Stats — Minijuegos.com

## Stats UIDs

Type: **REPLACE** — always send the accumulated total, never a delta.

| UID | Description |
|-----|-------------|
| `plays` | Total games played |
| `kills` | Total kills |
| `circle` | Highest circle/level reached |
| `wins` | Total wins |
| `gold` | Total gold collected |

```javascript
// Send after every game session (accumulated totals)
lechuck.set_stat('plays', totalPlays);
lechuck.set_stat('kills', totalKills);
lechuck.set_stat('circle', highestCircle);
lechuck.set_stat('wins', totalWins);
lechuck.set_stat('gold', totalGold);
```

## Achievement UIDs

Register these in the Minijuegos developer panel. Images: PNG 64×64.

| UID | Description | Difficulty |
|-----|-------------|-----------|
| `primera_sangre` | First blood | Easy |
| `primer_kill` | First kill | Easy |
| `iniciado` | Initiated | Easy |
| `superviviente` | Survivor | Easy |
| `explorador` | Explorer | Easy |
| `guerrero` | Warrior | Medium |
| `asesino_serie` | Serial killer | Medium |
| `campeon` | Champion | Medium |
| `cazador_oro` | Gold hunter | Medium |
| `veterano` | Veteran | Hard |
| `maestro` | Master | Hard |
| `genocida` | Genocidal | Hard |
| `elite` | Elite | Hard |
| `leyenda_oscura` | Dark Legend | Very Hard |
| `cazador_lucifer` | Lucifer Hunter | Very Hard |
| `leyenda` | Legend | Very Hard |
| `el_que_persiste` | The Persistent | Very Hard |

## Image Color Coding by Difficulty

- Easy → green background
- Medium → orange background
- Hard → red background
- Very Hard → purple background

## Unlock Pattern

Track which achievements have been unlocked per-user. Unlock only when the condition is first met:

```javascript
// Example: unlock on first kill
function onEnemyKilled(totalKills) {
  if (totalKills === 1 && !achievements.has('primer_kill')) {
    _mpUnlockAchievement('primer_kill');
    achievements.add('primer_kill');
  }
  if (totalKills >= 10 && !achievements.has('guerrero')) {
    _mpUnlockAchievement('guerrero');
    achievements.add('guerrero');
  }
  // etc.
}
```

## Note: Write Permissions

Minijuegos must enable write permissions for your API_ID in their panel before stats and achievements can be recorded. Contact Minijuegos support if `set_stat` / `unlockAchievement` calls appear to have no effect.
