console.log('bot service booting');
console.log('monorepo bot wired as service entrypoint; replace with full discord.js runtime when desired');
let beat = 0;
setInterval(() => {
  beat += 1;
  console.log(`bot heartbeat (${beat})`);
}, 15000);
