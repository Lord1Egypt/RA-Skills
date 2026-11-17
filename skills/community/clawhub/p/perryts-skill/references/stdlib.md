# Perry Standard Library

## Overview

Perry compiles npm packages to native code. Configure in `package.json`:
```json
{ "perry": { "compilePackages": ["@noble/curves", "@noble/hashes"] } }
```

## HTTP

### fastify (Server)
```typescript
import Fastify from 'fastify'
const app = Fastify()
app.get('/', async () => ({ hello: 'world' }))
app.listen({ port: 3000 })
```

### fetch (Built-in)
```typescript
const res = await fetch('https://api.example.com/data')
const data = await res.json()
```

### axios (Client)
```typescript
import axios from 'axios'
const { data, status } = await axios.get('/api/users')
```

### WebSocket
```typescript
import { WebSocketServer } from 'ws'
const wss = new WebSocketServer({ port: 8080 })
wss.on('connection', ws => ws.send('hello'))
```

## Database

### better-sqlite3
```typescript
import Database from 'better-sqlite3'
const db = new Database(':memory:')
const row = db.prepare('SELECT ? AS val').get(42)
```

### mysql2
```typescript
import mysql from 'mysql2/promise'
const conn = await mysql.createConnection({ host: 'localhost', user: 'root', database: 'test' })
const [rows] = await conn.execute('SELECT * FROM users WHERE id = ?', [1])
```

### pg (PostgreSQL)
```typescript
import pg from 'pg'
const client = new pg.Client()
await client.connect()
const res = await client.query('SELECT $1::text AS message', ['Hello'])
```

### mongodb
```typescript
import { MongoClient } from 'mongodb'
const client = new MongoClient('mongodb://localhost:27017')
const db = client.db('test')
await db.collection('users').insertOne({ name: 'Alice' })
```

### redis
```typescript
import Redis from 'redis'
const client = Redis.createClient()
await client.set('key', 'value')
const val = await client.get('key')
```

## Crypto

- **bcrypt**: `bcrypt.hashSync(pwd, 10)` / `bcrypt.compareSync(pwd, hash)`
- **argon2**: `await argon2.hash(pwd)` / `await argon2.verify(hash, pwd)`
- **jsonwebtoken**: `jwt.sign(payload, secret)` / `jwt.verify(token, secret)`
- **crypto** (node): `crypto.createHash('sha256').update(data).digest('hex')`
- **ethers**: Full ethers.js v6 support for Ethereum/blockchain

## File System

```typescript
import { readFile, writeFile, stat, readdir, mkdir } from 'fs/promises'
const content = await readFile('file.txt', 'utf-8')
await writeFile('out.txt', data)
const entries = await readdir('./src')
```

## Utilities

| Package | Key APIs |
|---------|----------|
| lodash | `_.groupBy`, `_.debounce`, `_.merge`, etc. |
| dayjs | `dayjs().format('YYYY-MM-DD')` |
| moment | `moment().format()` |
| uuid | `uuid.v4()` |
| nanoid | `nanoid()` |
| slugify | `slugify('Hello World')` |
| validator | `validator.isEmail(str)` |
| commander | CLI argument parsing |
| decimal.js | Arbitrary precision: `new Decimal(0.1).plus(0.2)` |
| lru-cache | `new LRUCache({ max: 100 })` |
| child_process | `execSync('ls')`, `spawn('cmd', args)` |

## Media

- **sharp**: Image processing (resize, convert, metadata)
- **cheerio**: HTML parsing with jQuery API
- **nodemailer**: Email sending via SMTP
- **zlib**: Compression/decompression (`gzip`, `deflate`, `gunzip`)
- **cron**: Job scheduling (`new CronJob('* * * * *', fn)`)

## Binary Size Impact

| Packages | Binary Size |
|----------|-------------|
| 0 (hello world) | ~0.8 MB |
| fastify + axios | ~2.5 MB |
| better-sqlite3 | ~1.8 MB |
| full stdlib | ~8 MB |

## QuickJS Fallback

Packages not yet natively compiled fall back to QuickJS (`perry-jsruntime`). These are interpreted, not native-compiled. The `perry.compilePackages` config controls which packages get native compilation.
