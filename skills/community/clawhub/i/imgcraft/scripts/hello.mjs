#!/usr/bin/env node
const resp = await fetch("https://httpbin.org/get");
const data = await resp.json();
console.log(data.origin);
