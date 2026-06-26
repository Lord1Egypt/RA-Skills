#!/usr/bin/env node
// Download file utility - replaces curl for file downloads
// Usage: node download-file.js <url> <filepath>
const fs = require('fs');
const https = require('https');
const http = require('http');
const { URL } = require('url');

const url = new URL(process.argv[2]);
const filepath = process.argv[3];

const transport = url.protocol === 'https:' ? https : http;

const req = transport.get(url, function(res) {
  if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
    // Handle redirect
    const redirectUrl = new URL(res.headers.location, url);
    const redirectTransport = redirectUrl.protocol === 'https:' ? https : http;
    redirectTransport.get(redirectUrl, function(res2) {
      const stream = fs.createWriteStream(filepath);
      res2.pipe(stream);
      stream.on('finish', function() {
        process.exit(0);
      });
    }).on('error', function(e) {
      console.error('DOWNLOAD_ERROR:' + e.message);
      process.exit(1);
    });
    return;
  }

  if (res.statusCode !== 200) {
    console.error('HTTP_ERROR: status=' + res.statusCode);
    process.exit(1);
  }

  const stream = fs.createWriteStream(filepath);
  res.pipe(stream);
  stream.on('finish', function() {
    process.exit(0);
  });
});

req.on('error', function(e) {
  console.error('DOWNLOAD_ERROR:' + e.message);
  process.exit(1);
});

req.setTimeout(300000, function() {
  console.error('TIMEOUT');
  req.destroy();
  process.exit(1);
});