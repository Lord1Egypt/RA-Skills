import express from 'express';
import { verifySVG } from './index.js';

const app = express();
app.use(express.text({ type: 'image/svg+xml', limit: '5mb' }));

/**
 * @api {post} /verify Verify a Nifty SVG
 * @apiDescription Verifies the cryptographic integrity and provenance chain of an SVG.
 */
app.post('/verify', async (req, res) => {
    try {
        const svg = req.body;
        if (!svg || svg.trim().length === 0) {
            return res.status(400).json({ error: 'Missing SVG body' });
        }

        if (!svg.includes('<svg')) {
            return res.status(400).json({ error: 'Invalid SVG format' });
        }

        const result = await verifySVG(svg);
        
        if (!result.isValid) {
            return res.status(200).json({
                ...result,
                error: result.metadata?.hash 
                    ? 'Signature verification failed or chain integrity compromised'
                    : 'No valid NASP metadata found'
            });
        }
        
        res.json(result);
    } catch (e) {
        const error = e as Error;
        
        // Log full error for debugging
        console.error('Verification error:', error);
        
        // Return appropriate status based on error type
        if (error.message.includes('No NASP metadata')) {
            return res.status(400).json({
                isValid: false,
                error: 'No NASP metadata found in SVG'
            });
        }
        
        if (error.message.includes('Base64') || error.message.includes('JSON')) {
            return res.status(400).json({
                isValid: false,
                error: 'Corrupted metadata format'
            });
        }
        
        res.status(500).json({
            isValid: false,
            error: 'Internal verification error'
        });
    }
});

app.get('/health', (req, res) => {
    res.json({ status: 'ok', service: 'nifty-agents-protocol-verification' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`🚀 NASP Verification Server running on port ${PORT}`);
});
