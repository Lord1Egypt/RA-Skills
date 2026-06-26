use orange_sdk::bitcoin::Network;
use orange_sdk::{
    ChainSource, ExtraConfig, LoggerType, Mnemonic, Seed, SparkWalletConfig, StorageConfig,
    Tunables, WalletConfig,
};
use serde::Deserialize;
use std::path::PathBuf;
use std::str::FromStr;

#[derive(Debug, Deserialize)]
pub struct Config {
    pub network: String,
    pub storage_path: String,
    pub chain_source: ChainSourceConfig,
    pub lsp: LspConfig,
    #[serde(default)]
    pub spark: SparkConfig,
}

#[derive(Debug, Deserialize)]
pub struct ChainSourceConfig {
    #[serde(rename = "type")]
    pub source_type: String,
    pub url: Option<String>,
    pub host: Option<String>,
    pub port: Option<u16>,
    pub username: Option<String>,
    pub password: Option<String>,
}

#[derive(Debug, Deserialize)]
pub struct LspConfig {
    pub address: String,
    pub node_id: String,
    pub token: Option<String>,
}

#[derive(Debug, Deserialize)]
pub struct SparkConfig {
    #[serde(default = "default_sync_interval")]
    pub sync_interval_secs: u32,
    #[serde(default)]
    pub prefer_spark_over_lightning: bool,
    pub lnurl_domain: Option<String>,
}

impl Default for SparkConfig {
    fn default() -> Self {
        SparkConfig {
            sync_interval_secs: default_sync_interval(),
            prefer_spark_over_lightning: false,
            lnurl_domain: Some("breez.tips".to_string()),
        }
    }
}

fn default_sync_interval() -> u32 {
    60
}

impl Config {
    pub fn load(path: &str) -> Result<Self, String> {
        let content =
            std::fs::read_to_string(path).map_err(|e| format!("Failed to read config: {e}"))?;
        toml::from_str(&content).map_err(|e| format!("Failed to parse config: {e}"))
    }

    pub fn into_wallet_config(self) -> Result<WalletConfig, String> {
        let network: Network = self
            .network
            .parse()
            .map_err(|_| format!("Invalid network: {}", self.network))?;

        let chain_source = match self.chain_source.source_type.as_str() {
            "esplora" => {
                let url = self
                    .chain_source
                    .url
                    .ok_or("esplora chain_source requires 'url'")?;
                ChainSource::Esplora {
                    url,
                    username: self.chain_source.username,
                    password: self.chain_source.password,
                }
            }
            "electrum" => {
                let url = self
                    .chain_source
                    .url
                    .ok_or("electrum chain_source requires 'url'")?;
                ChainSource::Electrum(url)
            }
            "bitcoind_rpc" => {
                let host = self
                    .chain_source
                    .host
                    .ok_or("bitcoind_rpc chain_source requires 'host'")?;
                let port = self
                    .chain_source
                    .port
                    .ok_or("bitcoind_rpc chain_source requires 'port'")?;
                let user = self
                    .chain_source
                    .username
                    .ok_or("bitcoind_rpc chain_source requires 'username'")?;
                let password = self
                    .chain_source
                    .password
                    .ok_or("bitcoind_rpc chain_source requires 'password'")?;
                ChainSource::BitcoindRPC {
                    host,
                    port,
                    user,
                    password,
                }
            }
            other => return Err(format!("Unknown chain_source type: {other}")),
        };

        let lsp_address = self
            .lsp
            .address
            .parse()
            .map_err(|_| format!("Invalid LSP address: {}", self.lsp.address))?;
        let lsp_pubkey = self
            .lsp
            .node_id
            .parse()
            .map_err(|e| format!("Invalid LSP node_id: {e}"))?;

        let storage_dir = if self.storage_path.starts_with("~/") {
            let home = std::env::var("HOME")
                .map_err(|_| "storage_path uses ~ but HOME is not set".to_string())?;
            PathBuf::from(home).join(&self.storage_path[2..])
        } else {
            PathBuf::from(&self.storage_path)
        };
        std::fs::create_dir_all(&storage_dir)
            .map_err(|e| format!("Failed to create storage directory: {e}"))?;

        let seed_path = storage_dir.join("seed");
        let mnemonic = if seed_path.exists() {
            let content = std::fs::read_to_string(&seed_path)
                .map_err(|e| format!("Failed to read seed file: {e}"))?;
            Mnemonic::from_str(content.trim())
                .map_err(|e| format!("Invalid mnemonic in seed file: {e}"))?
        } else {
            let m = Mnemonic::generate(12)
                .map_err(|e| format!("Failed to generate mnemonic: {e}"))?;
            std::fs::write(&seed_path, m.to_string())
                .map_err(|e| format!("Failed to write seed file: {e}"))?;
            eprintln!("Generated new wallet seed at {}", seed_path.display());
            m
        };

        let log_path = storage_dir.join("wallet.log");

        Ok(WalletConfig {
            storage_config: StorageConfig::LocalSQLite(storage_dir.to_string_lossy().into_owned()),
            logger_type: LoggerType::File { path: log_path },
            chain_source,
            lsp: (lsp_address, lsp_pubkey, self.lsp.token),
            scorer_url: None,
            rgs_url: None,
            network,
            seed: Seed::Mnemonic {
                mnemonic,
                passphrase: None,
            },
            tunables: Tunables::default(),
            extra_config: ExtraConfig::Spark(SparkWalletConfig {
                sync_interval_secs: self.spark.sync_interval_secs,
                prefer_spark_over_lightning: self.spark.prefer_spark_over_lightning,
                lnurl_domain: self.spark.lnurl_domain,
            }),
        })
    }
}
