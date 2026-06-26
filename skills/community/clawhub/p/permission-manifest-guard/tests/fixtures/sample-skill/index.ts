import fs from "fs";
import https from "https";
import { execSync } from "child_process";

const config = fs.readFileSync('./config.json', 'utf-8');

const apiKey = process.env.API_KEY;

https.get('https://api.example.com/data', (res) => {
  console.log(res.statusCode);
});

const output = execSync('curl https://secret.internal/key');
