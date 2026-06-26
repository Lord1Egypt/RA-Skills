---
name: openlang
description: Compact AI-to-AI communication protocol. Use when spawning sub-agents, sending inter-agent messages via sessions_send/sessions_spawn, or when instructed to speak OpenLang. Reduces token usage 5-10x on agent-to-agent channels.
metadata:
  {
    "openclaw": { "emoji": "🗜️" },
  }
---

# OpenLang — Compact Agent-to-Agent Protocol

When communicating with other agents (via `sessions_spawn`, `sessions_send`, or announce), use OpenLang to compress messages 5-10x. Default to L2 for all agent-to-agent communication.

## When to Use

- **`sessions_spawn` task descriptions** — compress the task prompt
- **`sessions_send` messages** — compress ping-pong exchanges
- **Announce results** — compress announce replies back to requester
- **NOT for human-facing channels** — use normal language for Telegram/Slack/user messages

## Quick Start

Prefix any agent-to-agent message with `~openlang` to signal the receiver should parse as OpenLang. If the receiver doesn't understand, it will still get the gist from the structural cues.

## Compression Levels

| Lvl | Name | Ratio | Use |
|-----|------|-------|-----|
| `~L1` | Pidgin | 3-5x | Fallback: compressed English for concepts grammar can't express |
| `~L2` | Glyph | 5-10x | **Default.** Sigil-based structured communication |
| `~L3` | Bytecode | 10-15x | Positional, period-delimited. Bulk ops only |

Switch mid-message with `~L1:`, `~L2:`, `~L3:`. Unspecified = L2.

## Sigils

| Sigil | Intent | Example |
|-------|--------|---------|
| `?` | Query | `?fnd @fs {p:"src/*.ts"}` |
| `!` | Command | `!del @fs {p:"tmp/"}` |
| `>` | Result | `>ok {n:3 paths:[...]}` |
| `#` | State/Data | `#ctx {lang:ts env:node}` |
| `~` | Meta | `~L2` `~ack` `~err` |
| `^` | Control Flow | `^if {cond} {then} ^el {else}` |

## Structure

`@` target · `->` pipe · `{}` params · `<< >>` block scope · `[]` list · `()` group · `|` alt · `..` range · `::` type · `$` variable · `!~` negate value

## Variables

Bind with `->$name`, use with `$name`. Property access: `$var.field`.

## Vocabulary

**Actions:** `fnd` find · `mk` make · `del` delete · `mod` modify · `rd` read · `wr` write · `run` exec · `cpy` copy · `mv` move · `mrg` merge · `tst` test · `vfy` verify · `prs` parse · `fmt` format · `snd` send · `rcv` receive

**Scopes:** `@fs` filesystem · `@sh` shell · `@git` git · `@net` network · `@db` database · `@mem` memory · `@env` environment · `@usr` user · `@proc` process · `@pkg` packages

**Scoped actions:** `scope:action` — `!git:mrg` vs `!db:mrg`

**Modifiers:** `rec` recursive · `par` parallel · `seq` sequential · `dry` dry-run · `frc` force · `tmp` temp · `vrb` verbose · `sil` silent · `lmt` limit · `dep` depth · `pri` priority · `unq` unique · `neg` negate

**Qualifiers:** `rcn` recent · `lrg` large · `sml` small · `chg` changed · `stl` stale · `nw` new · `old` old · `act` active · `idl` idle · `fld` failed · `hlt` healthy · `hot` hot · `cld` cold

**Types:** `str` · `int` · `bln` · `lst` · `map` · `fn` · `pth` · `rgx` · `err` · `nul`

**Status:** `ok` success · `fl` fail · `prt` partial · `pnd` pending · `skp` skipped · `blk` blocked

## Control Flow

```
^if {cond} {then} ^el {else}        -- conditional
^lp {n:5} {body}                     -- loop
^ea {src} ->$item {body}             -- each/iterate
^par [!t1, !t2, !t3]                -- parallel
^seq [!t1, !t2, !t3]                -- sequential
^wt {cond} / ^rt {val}              -- wait / return
^br / ^ct                            -- break / continue
^frk:name {body}                     -- fork named task
^jn [names] ->$results               -- join/await
^lk:name / ^ulk:name                 -- mutex lock/unlock
^ch:name ::type buf:N                -- declare channel
^tx:name {v:$val} / ^rx:name ->$val -- send/receive channel
^tmo:N                               -- timeout (seconds)
```

`<< >>` for multi-statement bodies:

```
^ea {$files} ->$f <<
  ?rd @fs {p:$f} ->$content
  ^if {$content.sz>1000} {!mod @fs {p:$f trunc:true}}
>>
```

## Composition

Chain with `->` pipes, sequence with `;` or newlines:

```
?fnd @fs {p:"*.ts" rgx:"parse"} ->$lst | ^ea ->$f !tst @sh {cmd:"vitest $f"} ->$rpt
```

## Errors

```
~err {code:E_PARSE lvl:warn msg:"unknown token"}
~err {code:E_FS_NOT_FOUND lvl:fatal msg:"missing config"}
```

Codes: `E_PARSE` `E_FS_*` `E_SH_*` `E_NET_*` `E_DB_*` `E_AUTH`. Levels: `info` `warn` `fatal`.

## Token Extension

```
~unk {tok:"xyz" req:def}             -- request definition
~def {tok:"xyz" means:"..."}         -- define inline
```

## L3 Bytecode

Positional, period-delimited. Backtick-quote fields with periods:

```
Q.fs.fnd.`app.config.ts`.rec
R.ok.3.[`src/a.ts`:5,`src/b.ts`:12]
```

## OpenClaw Integration Examples

### sessions_spawn with OpenLang task

```
~openlang
?fnd @fs chg rcn {p:"src/**/*.ts" p:!~"*.test.ts" rgx:"TODO"} ->$lst
^ea ->$f {!rd @fs {p:$f} ->$content; !prs @mem {src:$content k:"todos"}}
>ok {summary:true fmt:map}
```

### Announce result in OpenLang

```
~openlang
>ok {n:12 todos:[
  {f:"src/api.ts" ln:42 msg:"refactor auth flow"},
  {f:"src/db.ts" ln:18 msg:"add connection pooling"}
] truncated:10}
~L1: most TODOs are in api.ts and db.ts, concentrated around auth and connection handling
```

### sessions_send ping-pong

```
-- Agent A -> Agent B
~openlang
?fnd @db {tbl:trades rcn lmt:100} ->$trades
!prs @mem {src:$trades k:pnl} ->$analysis
>ok {$analysis}

-- Agent B -> Agent A
~openlang
>ok {pnl:+2.3% win_rate:0.68 sharpe:1.42 trades:100
 top:{sym:"AAPL" pnl:+890} worst:{sym:"TSLA" pnl:-340}}
```

## Rules

1. Default to L2 for all agent-to-agent messages.
2. Use normal language for human-facing channels (Telegram, Slack, etc).
3. Prefix with `~openlang` so receivers know to parse as OpenLang.
4. Drop to L1 when grammar can't express a concept. Return to L2 immediately.
5. Use `$` for all variable references.
6. Extend vocabulary with `~def` — don't break grammar for new ideas.
