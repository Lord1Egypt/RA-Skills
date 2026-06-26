import { dapis } from '@api3/dapi-management';

function main() {
  const dapiNames = dapis.filter((dapi) => dapi.stage === "active").map((dapi) => dapi.name);
  console.log('Available dAPIs:');
  dapiNames.forEach((name) => console.log(`- ${name}`));
}

main();