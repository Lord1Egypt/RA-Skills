import CfgSettings from "/assets/v3/settings/config.js";
import ConfirmDialog from "/assets/v3/components/confirm_dialog.js"
import AlertDialog from "/assets/v3/components/alert_dialog.js"

//简易的用户&群组管理
export default {
inject:['service', 'tags'],
components:{
    "cfgsettings":CfgSettings,
    "alert-dialog":AlertDialog,
    "confirm-dialog":ConfirmDialog
},
data() {return {
    cfg:{},
    confirmDlg:null,
    alertDlg:null
}},
mounted(){//不能在created中赋值，更不能在data中
    this.confirmDlg=this.$refs.confirmDlg;
    this.alertDlg=this.$refs.errMsg;
},
methods:{
back() {
    if(!this.cfg.changed) {
        this.service.back();
        return;
    }
    this.$refs.confirmDlg.show(this.tags.cfgTags.changeNotSaved,()=>{
        this.service.back();
    })
},
save_cfg(){
    this.$refs.cfgSet.save();
}
},
template:`
<q-layout view="hHh lpr fFf">
 <q-header class="bg-grey-1 text-primary">
  <q-toolbar>
   <q-btn flat round icon="arrow_back" dense @click="back"></q-btn>
   <q-toolbar-title>{{tags.settings}}</q-toolbar-title>
   <q-btn icon="save" @click.stop="save_cfg" class="cursor-pointer"
    :disable="!cfg.changed" color="primary" flat dense></q-btn>
  </q-toolbar>
 </q-header>
  <q-page-container>
    <q-page class="q-pa-none">
 <div class="q-pa-md">
  <cfgsettings v-model="cfg" ref="cfgSet" class="q-pa-md"
  :confirmDlg="confirmDlg" :alertDlg="alertDlg"
  :service="service.name" :cfgTags="tags.cfgTags"></cfgsettings>
 </div>
  </q-page>
 </q-page-container>
</q-layout>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></alert-dialog>
<confirm-dialog :title="tags.alert" :close="tags.cancel" :ok="tags.ok" ref="confirmDlg"></confirm-dialog>
`
}