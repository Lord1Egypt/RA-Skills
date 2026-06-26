console.log('worker service booting');
let n = 0;
setInterval(() => {
  n += 1;
  console.log(`worker polling jobs (${n})`);
}, 5000);
