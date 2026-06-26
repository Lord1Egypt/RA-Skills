import 'dotenv/config';
import { drizzle } from 'drizzle-orm/node-postgres';
import { Client } from 'pg';
import { guildSettings } from './schema.js';

const client = new Client({ connectionString: process.env.DATABASE_URL });
await client.connect();
const db = drizzle(client);

const rows = await db.select().from(guildSettings).limit(10);
console.log(rows);

await client.end();
