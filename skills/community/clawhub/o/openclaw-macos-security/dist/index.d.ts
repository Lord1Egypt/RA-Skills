/**
 * MaclawPro Security - OpenClaw Skill
 * Professional macOS security monitoring
 *
 * Created by SEQUR.ca - Certified Cybersecurity Experts
 * https://maclawpro.com
 */
/**
 * Skill metadata for OpenClaw
 */
export declare const metadata: {
    name: string;
    displayName: string;
    description: string;
    version: string;
    author: string;
    homepage: string;
    category: string;
    icon: string;
    commands: string[];
};
/**
 * Camera status check
 */
export declare function cameraStatus(): Promise<string>;
/**
 * Microphone status check
 */
export declare function microphoneStatus(): Promise<string>;
/**
 * Firewall status
 */
export declare function firewallStatus(): Promise<string>;
/**
 * VPN checker
 */
export declare function vpnChecker(): Promise<string>;
/**
 * Open ports scanner
 */
export declare function openPorts(): Promise<string>;
/**
 * WiFi scanner
 */
export declare function wifiScanner(): Promise<string>;
/**
 * Block app (simplified version)
 */
export declare function blockApp(appName: string): Promise<string>;
/**
 * Main skill export for OpenClaw
 */
declare const _default: {
    metadata: {
        name: string;
        displayName: string;
        description: string;
        version: string;
        author: string;
        homepage: string;
        category: string;
        icon: string;
        commands: string[];
    };
    commands: {
        'camera-status': typeof cameraStatus;
        'microphone-status': typeof microphoneStatus;
        'firewall-status': typeof firewallStatus;
        'vpn-checker': typeof vpnChecker;
        'open-ports': typeof openPorts;
        'wifi-scanner': typeof wifiScanner;
        'block-app': typeof blockApp;
    };
};
export default _default;
