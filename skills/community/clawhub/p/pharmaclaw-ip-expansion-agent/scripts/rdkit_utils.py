# RDKit utilities for IP analysis.
from rdkit import Chem, DataStructs
from rdkit.Chem import rdMolDescriptors

def get_fp(smiles: str, radius: int = 2, nbits: int = 2048):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return rdMolDescriptors.GetMorganFingerprintAsBitVect(mol, radius, nbits)

def tanimoto(fp1, fp2):
    return DataStructs.TanimotoSimilarity(fp1, fp2)

def suggest_derivatives(smiles: str):
    # Placeholder for more advanced (e.g., enumerate)
    mol = Chem.MolFromSmiles(smiles)
    # Example: Add functional groups
    rwmol = Chem.RWMol(mol)
    # ... advanced logic
    return [Chem.MolToSmiles(mol)]  # Stub
