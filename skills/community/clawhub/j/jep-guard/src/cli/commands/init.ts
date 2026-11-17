import {Command} from 'commander';
import inquirer from 'inquirer';
import fs from 'fs';
import path from 'path';
export const initCommand=new Command('init').description('Create an explicit local Guard configuration').action(async()=>{
 const {dir,secureDir}=require('../../../transport');
 const {mode}=await inquirer.prompt([{type:'list',name:'mode',message:'Runtime policy mode',choices:[{name:'Passive: no execution protection',value:'passive'},{name:'Full: block unless authenticated policy grants execution',value:'full'}],default:'passive'}]);
 secureDir(dir());
 fs.writeFileSync(path.join(dir(),'config.json'),JSON.stringify({version:'3.0.0',mode},null,2),{mode:0o600,flag:'wx'});
 console.log('Configuration created. Provision trusted skill keys, allowed-skills.json and policy.json before starting the daemon.');
});
