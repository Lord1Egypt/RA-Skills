# GPU Pricing Reference Data
# Last Updated: 2026-04-16
# Data Sources: AWS/GCP/Azure/Volcengine/Alibaba Cloud official pricing pages

## AWS GPU Instances

| Instance | GPU | VRAM | vCPUs | Memory | On-Demand ($/hr) | 1yr RI ($/hr) | 3yr RI ($/hr) | Network | Storage |
|----------|-----|------|-------|--------|-----------------|---------------|---------------|---------|---------|
| p5en.48xlarge | H100 SXM 80GB | 80GB HBM3 | 192 | 2048GB | $98.32 | ~$58.99 | ~$44.24 | 3200 Gbps | EBS Only |
| p4d.24xlarge | A100 80GB | 80GB HBM2e | 96 | 1152GB | $40.50 | ~$24.30 | ~$18.23 | 400 Gbps | 8TB NVMe |
| p4de.24xlarge | A100 80GB | 80GB HBM2e | 96 | 1152GB | $55.86 | ~$33.52 | ~$25.14 | 400 Gbps | 8TB NVMe |
| g6.48xlarge | L40S | 48GB | 192 | 2048GB | $22.05 | ~$13.23 | ~$9.92 | 3200 Gbps | EBS Only |
| g5.48xlarge | A10G | 24GB | 192 | 2048GB | $12.24 | ~$7.34 | ~$5.51 | 3200 Gbps | 7.6TB NVMe |

**Regions (us-east-1):** p5en.48xlarge, p4d.24xlarge, g6.48xlarge, g5.48xlarge

## GCP GPU Instances

| Machine Type | GPU | VRAM | vCPUs | Memory | On-Demand ($/hr) | 1yr CUD ($/hr) | 3yr CUD ($/hr) | Network | Max GPUs |
|-------------|-----|------|-------|--------|-----------------|----------------|----------------|---------|----------|
| a3-highgpu-8g | H100 SXM 80GB | 80GB HBM3 | 208 | 2048GB | $105.46 | ~$63.28 | ~$47.46 | 200 Gbps | 8 |
| a2-highgpu-1g | A100 80GB | 80GB HBM2e | 12 | 170GB | $11.36 | ~$6.82 | ~$5.11 | 32 Gbps | 1 |
| a2-highgpu-4g | A100 80GB | 80GB HBM2e | 48 | 680GB | $40.33 | ~$24.20 | ~$18.15 | 100 Gbps | 4 |
| g2-standard-4 | L4 | 24GB | 16 | 64GB | $1.22 | ~$0.73 | ~$0.55 | 20 Gbps | 1 |
| g2-standard-8 | L4 | 24GB | 32 | 128GB | $2.44 | ~$1.46 | ~$1.10 | 20 Gbps | 1 |
| g2-standard-12 | L4 | 24GB | 48 | 192GB | $3.66 | ~$2.20 | ~$1.65 | 20 Gbps | 1 |

**Regions:** us-central1, us-east1, europe-west4
**Note:** GCP sustained use discounts (SUD) apply automatically. CUD = Committed Use Discount.

## Azure GPU Instances

| VM Size | GPU | VRAM | vCPUs | Memory | On-Demand ($/hr) | 1yr RI ($/hr) | 3yr RI ($/hr) | Network | Storage |
|---------|-----|------|-------|--------|-----------------|----------------|----------------|---------|---------|
| ND H100 v5 | H100 SXM 80GB | 80GB HBM3 | 224 | 2048GB | $104.40 | ~$62.64 | ~$46.98 | 3200 Gbps | 6.4TB NVMe |
| NC A100 v4 | A100 80GB | 80GB HBM2e | 96 | 900GB | $39.82 | ~$23.89 | ~$17.92 | 80 Gbps | 2.88TB NVMe |
| NV L40s | L40S | 48GB | 72 | 900GB | $14.40 | ~$8.64 | ~$6.48 | 80 Gbps | 1.8TB NVMe |
| NC A10 v2 | A10G | 24GB | 24 | 220GB | $3.67 | ~$2.20 | ~$1.65 | 50 Gbps | 360GB NVMe |

**Regions:** eastus, westus3, westeurope, southeastasia

## 火山引擎 (Volcengine) GPU Instances

| Instance Type | GPU | VRAM | vCPUs | Memory | On-Demand ($/hr) | 1yr ($/hr) | 3yr ($/hr) | Network | Storage |
|--------------|-----|------|-------|--------|-----------------|------------|------------|---------|---------|
| ecs.vgh.8xlarge | H100 SXM 80GB | 80GB HBM3 | 64 | 512GB | ~$12.50 | ~$7.50 | ~$5.00 | 100 Gbps | 500GB SSD |
| ecs.vga.4xlarge | A100 80GB | 80GB HBM2e | 32 | 256GB | ~$6.20 | ~$3.72 | ~$2.48 | 50 Gbps | 500GB SSD |
| ecs.vgl.4xlarge | L40S | 48GB | 32 | 256GB | ~$3.80 | ~$2.28 | ~$1.52 | 50 Gbps | 500GB SSD |

**Regions:** cn-beijing, cn-shanghai, ap-southeast-1

## 阿里云 (Alibaba Cloud) GPU Instances

| Instance Type | GPU | VRAM | vCPUs | Memory | On-Demand ($/hr) | 1yr ($/hr) | 3yr ($/hr) | Network | Storage |
|--------------|-----|------|-------|--------|-----------------|------------|------------|---------|---------|
| ecs.ebmgn7.26xlarge | H100 SXM 80GB | 80GB HBM3 | 104 | 768GB | ~$15.80 | ~$9.48 | ~$6.32 | 100 Gbps | 1TB SSD |
| ecs.gn7.26xlarge | A100 80GB | 80GB HBM2e | 104 | 768GB | ~$9.50 | ~$5.70 | ~$3.80 | 100 Gbps | 1TB SSD |
| ecs.gn7r.26xlarge | A100 40GB | 40GB HBM2e | 104 | 768GB | ~$7.20 | ~$4.32 | ~$2.88 | 100 Gbps | 1TB SSD |
| ecs.gn6v.10xlarge | V100 32GB | 32GB HBM2 | 40 | 480GB | ~$4.50 | ~$2.70 | ~$1.80 | 50 Gbps | 500GB SSD |
| ecs.gn6e.14xlarge | A10 | 24GB | 56 | 456GB | ~$3.20 | ~$1.92 | ~$1.28 | 50 Gbps | 500GB SSD |

**Regions:** cn-hangzhou, cn-shanghai, cn-beijing

## GPU Specifications Comparison

| GPU | Vendor | Memory | Bandwidth | FP16 TFLOPS | Architecture | TDP | Release |
|-----|--------|--------|-----------|-------------|--------------|-----|---------|
| H100 SXM | NVIDIA | 80GB HBM3 | 3.35 TB/s | 1979 | Hopper | 700W | 2022 |
| A100 80GB | NVIDIA | 80GB HBM2e | 2.0 TB/s | 1248 | Ampere | 400W | 2020 |
| A100 40GB | NVIDIA | 40GB HBM2e | 1.6 TB/s | 624 | Ampere | 400W | 2020 |
| L40S | NVIDIA | 48GB GDDR6 | 864 GB/s | 733 | Ada Lovelace | 350W | 2023 |
| L4 | NVIDIA | 24GB GDDR6 | 300 GB/s | 242 | Ada Lovelace | 72W | 2023 |
| A10G | NVIDIA | 24GB GDDR6 | 600 GB/s | 312 | Ampere | 150W | 2021 |
| V100 | NVIDIA | 32GB HBM2 | 900 GB/s | 125 | Volta | 300W | 2017 |

## Pricing Notes

1. 所有价格均为USD，按量付费价格不含税
2. AWS/GCP/Azure 价格为美区(us-east-1/us-central1/eastus)参考价
3. 火山引擎/阿里云价格为中国区参考价，实际以官网为准
4. 预留实例(RI)/承诺使用折扣(CUD)价格为估算值，实际需在官网计算
5. 网络带宽为实例最大带宽，实际性能取决于网络配置
6. 存储为本地NVMe/SSD容量，不含额外EBS费用
7. 价格会随云厂商政策调整，建议以官网最新定价为准
