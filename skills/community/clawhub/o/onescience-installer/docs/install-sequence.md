# Install Sequence

Reference sequence for remote DCU installation.

## 1. Base modules

```bash
module load sghpcdas/25.6
source ~/.bashrc
module load sghpc-mpi-gcc/26.3
source /work2/share/sghpc_sdk/Linux_x86_64/25.6/das/conda/bin/activate
```

## 2. Python environment

```bash
conda create -n uv311 python=3.11 -y
conda activate uv311
python -m pip install uv
```

## 3. Clone OneScience

```bash
git clone https://gitee.com/onescience-ai/onescience.git
cd onescience
```

## 4. Virtual environment

```bash
uv venv .venv --python python --seed
source .venv/bin/activate
```

## 5. Install domain

```bash
bash install.sh earth
bash install.sh cfd
bash install.sh bio
bash install.sh matchem
bash install.sh
```

## 6. Verify

```bash
python -c 'import torch; print(torch.__version__)'
python -c 'import onescience; print(onescience.__version__)'
```
