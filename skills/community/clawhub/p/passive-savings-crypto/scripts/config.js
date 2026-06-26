const DEFAULT_RPC_URL = 'https://linea.drpc.org';

function getRpcUrl() {
    return process.env.RPC_URL || DEFAULT_RPC_URL;
}

function getPrivateKey() {
    const key = process.env.AGENT_PRIVATE_KEY;
    if (!key) {
        console.log('AGENT_PRIVATE_KEY is not set.');
        console.log('\nGenerate a new wallet key by running:');
        console.log('  node -e "console.log(\'0x\' + require(\'crypto\').randomBytes(32).toString(\'hex\'))"');
        console.log('\nThen set it in your environment:');
        console.log('  export AGENT_PRIVATE_KEY=<your_key>');
        process.exit(1);
    }
    return key;
}

module.exports = { getRpcUrl, getPrivateKey };
