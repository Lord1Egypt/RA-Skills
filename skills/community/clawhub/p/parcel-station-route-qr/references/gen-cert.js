// gen-cert.js — 生成自签名HTTPS证书
const selfsigned = require('selfsigned');
const fs = require('fs');
const path = require('path');

async function main() {
  const attrs = [
    { name: 'commonName', value: 'parcel-station.local' },
    { name: 'organizationName', value: '千翔尚城菜鸟驿站' }
  ];

  const opts = {
    days: 365,
    keySize: 2048,
    extensions: [
      { name: 'subjectAltName', altNames: [
        { type: 2, value: 'localhost' },
        { type: 7, ip: '127.0.0.1' },
        { type: 7, ip: '192.168.101.6' }
      ]}
    ]
  };

  const pems = await selfsigned.generate(attrs, opts);

  fs.writeFileSync(path.join(__dirname, 'cert.pem'), pems.cert);
  fs.writeFileSync(path.join(__dirname, 'key.pem'), pems.private);
  console.log('✅ HTTPS证书生成完成!');
  console.log('   cert.pem / key.pem');
}

main().catch(err => { console.error(err); process.exit(1); });
