import { execFile } from 'child_process';
import { promisify } from 'util';
import * as path from 'path';
import fs from "fs-extra";
import { fileURLToPath } from 'url';
const execFileAsync = promisify(execFile);
export class CxpWrapper {
    binaryPath;
    constructor(binaryPath) {
        if (binaryPath) {
            this.binaryPath = binaryPath;
        }
        else {
            // Robust __dirname for ESM
            const __filename = fileURLToPath(import.meta.url);
            const __dirname = path.dirname(__filename);
            let binaryName = 'cxp';
            const platform = process.platform;
            const arch = process.arch;
            if (platform === 'win32') {
                binaryName = 'cxp.exe';
            }
            else if (platform === 'linux') {
                binaryName = 'cxp-linux';
            }
            else if (platform === 'darwin') {
                if (arch === 'arm64') {
                    binaryName = 'cxp-arm64';
                }
                else {
                    binaryName = 'cxp';
                }
            }
            this.binaryPath = path.resolve(__dirname, '../bin', binaryName);
        }
    }
    async run(args) {
        try {
            // Ensure binary is executable
            if (process.platform !== 'win32') {
                try {
                    await fs.chmod(this.binaryPath, 0o755);
                }
                catch (e) { }
            }
            // Safety: 60s timeout for build/query
            const { stdout } = await execFileAsync(this.binaryPath, args, {
                timeout: 60000,
                killSignal: 'SIGKILL'
            });
            return stdout;
        }
        catch (error) {
            // Identify timeout explicitly
            if (error.code === 'SIGKILL' || (error.killed && error.signal === 'SIGKILL')) {
                const msg = `[Muninn] CXP Timeout: Command killed after 30s to protect system stability. Args: ${args.join(' ')}`;
                console.error(msg);
                throw new Error("Timeout: The brain query took too long and was terminated safely.");
            }
            throw new Error(`CXP command failed: ${error.message}\nStderr: ${error.stderr}`);
        }
    }
    async build(sourceDir, outputFile) {
        await this.run(['build', sourceDir, outputFile]);
    }
    async info(cxpPath) {
        return await this.run(['info', cxpPath]);
    }
    async query(cxpPath, query, topK = 10) {
        // The CLI output is designed for humans currently, so we return the raw output.
        // In a future iteration, we might want the CLI to output JSON mode.
        return await this.run(['query', cxpPath, query, '--top-k', topK.toString()]);
    }
    async search(cxpPath, query, topK = 10, modelPath) {
        return await this.run(['search', cxpPath, query, '--top-k', topK.toString(), '--model', modelPath]);
    }
    async ensureBinaryExists() {
        return await fs.pathExists(this.binaryPath);
    }
}
